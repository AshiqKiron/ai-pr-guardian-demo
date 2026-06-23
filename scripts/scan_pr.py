#!/usr/bin/env python3
"""
AI-PR Guardian: Automated PR Security Scanner
"""

import json
import os
import re
import sys
import argparse
from pathlib import Path

try:
    import yaml
except ImportError:
    print(" PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


class PolicyEngine:
    """Loads and manages security policies from YAML"""
    
    def __init__(self, policy_file):
        self.policy_file = policy_file
        self.policies = self._load_policies()
    
    def _load_policies(self):
        """Load policies from YAML file"""
        try:
            with open(self.policy_file, 'r') as f:
                config = yaml.safe_load(f)
            
            policies = config.get('policies', [])
            active_policies = [p for p in policies if p.get('enabled', True)]
            
            print(f"✅ Loaded {len(active_policies)} active policies from {self.policy_file}")
            return active_policies
            
        except FileNotFoundError:
            print(f"❌ Policy file not found: {self.policy_file}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error loading policies: {e}")
            sys.exit(1)
    
    def get_active_policies(self):
        return self.policies


class CodeScanner:
    """Scans code files for policy violations"""
    
    def __init__(self):
        self.violations = []
    
    def scan_with_regex(self, content, rule, filename):
        """Scan file content using regex pattern"""
        violations = []
        
        try:
            pattern = re.compile(rule['pattern'], re.IGNORECASE | re.MULTILINE)
            matches = pattern.finditer(content)
            
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                
                violation = {
                    'type': 'regex',
                    'rule_id': rule.get('id', 'unknown'),
                    'message': rule['message'],
                    'file': filename,
                    'line': line_num,
                    'matched_text': match.group()[:100],
                    'recommendation': rule.get('recommendation', '')
                }
                violations.append(violation)
                
        except re.error as e:
            print(f"⚠️ Regex error in rule {rule.get('id', 'unknown')}: {e}")
        
        return violations
    
    def check_file_content(self, filepath, rule):
        """Check if file contains required text"""
        violations = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(2000)
            
            required_text = rule.get('text', '')
            if required_text.lower() not in content.lower():
                violations.append({
                    'type': 'file_check',
                    'rule_id': rule.get('id', 'unknown'),
                    'message': rule['message'],
                    'file': str(filepath),
                    'recommendation': rule.get('recommendation', '')
                })
        except Exception as e:
            print(f"⚠️ Error reading file {filepath}: {e}")
        
        return violations
    
    def scan_file(self, filepath, policies):
        """Scan a single file against all policies"""
        file_violations = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️ Cannot read {filepath}: {e}")
            return []
        
        for policy in policies:
            policy_name = policy['name']
            severity = policy['severity']
            
            for rule in policy.get('rules', []):
                if rule['type'] == 'regex':
                    violations = self.scan_with_regex(content, rule, filepath)
                    for v in violations:
                        v['policy'] = policy_name
                        v['severity'] = severity
                        file_violations.append(v)
                
                elif rule['type'] == 'file_check':
                    file_ext = Path(filepath).suffix
                    if file_ext in rule.get('extensions', []):
                        violations = self.check_file_content(filepath, rule)
                        for v in violations:
                            v['policy'] = policy_name
                            v['severity'] = severity
                            file_violations.append(v)
        
        return file_violations


def get_changed_files_from_pr(pr_number, repo, token):
    """Get list of changed files in a PR using GitHub API"""
    import urllib.request
    
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            files = json.loads(response.read().decode())
        
        skip_extensions = {'.lock', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf'}
        filtered_files = [
            f['filename'] for f in files 
            if not any(f['filename'].endswith(ext) for ext in skip_extensions)
        ]
        
        return filtered_files
        
    except Exception as e:
        print(f"⚠️ Could not fetch PR files: {e}")
        return []


def scan_pr(pr_number, repo, policy_file, output_file='scan_results.json'):
    """Main scanning function"""
    
    print("\n" + "="*60)
    print("🛡️  AI-PR Guardian - Security Scanner")
    print("="*60)
    print(f" PR: #{pr_number}")
    print(f"📁 Repository: {repo}")
    print("="*60 + "\n")
    
    engine = PolicyEngine(policy_file)
    policies = engine.get_active_policies()
    
    token = os.environ.get('GITHUB_TOKEN', '')
    
    print(" Fetching changed files...")
    if token:
        changed_files = get_changed_files_from_pr(pr_number, repo, token)
    else:
        print("💡 Scanning local files (no GITHUB_TOKEN)")
        changed_files = []
        for ext in ['*.py', '*.js', '*.ts']:
            changed_files.extend([str(p) for p in Path('.').rglob(ext)])
    
    print(f" Found {len(changed_files)} files to scan\n")
    
    scanner = CodeScanner()
    all_violations = []
    files_scanned = 0
    
    for filename in changed_files:
        if not os.path.exists(filename):
            continue
        
        files_scanned += 1
        print(f"  [{files_scanned}] Scanning: {filename}")
        
        violations = scanner.scan_file(filename, policies)
        if violations:
            print(f"      ️  Found {len(violations)} violation(s)")
            all_violations.extend(violations)
    
    results = {
        'pr_number': pr_number,
        'repository': repo,
        'files_scanned': files_scanned,
        'violations_found': len(all_violations),
        'violations': all_violations,
        'status': 'blocked' if all_violations else 'approved',
        'policies_checked': len(policies)
    }
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*60)
    print(" SCAN SUMMARY")
    print("="*60)
    print(f"✅ Files scanned: {files_scanned}")
    print(f"{'❌' if all_violations else '✅'} Violations found: {len(all_violations)}")
    print(f"📈 Status: {results['status'].upper()}")
    print("="*60 + "\n")
    
    return results


def main():
    parser = argparse.ArgumentParser(description='AI-PR Guardian Scanner')
    parser.add_argument('--pr-number', type=int, required=True)
    parser.add_argument('--repository', type=str, required=True)
    parser.add_argument('--policies', type=str, default='.ai-guardrails/policies.yaml')
    parser.add_argument('--output', type=str, default='scan_results.json')
    
    args = parser.parse_args()
    
    # FIXED: Ensured all parentheses are properly closed
    results = scan_pr(
        pr_number=args.pr_number,
        repository=args.repository,
        policy_file=args.policies,
        output_file=args.output
    )
    
    if results['violations_found'] > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()

"""Optional GitHub REST adapter. Credentials come only from the process environment."""
import json
import os
from urllib.request import Request, build_opener, HTTPRedirectHandler


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError('Redirect refused; verify the repository target')


class GitHubIssues:
    """Create one issue; journal handles duplicate attempts, no HTTP auto-retries."""
    def __init__(self, opener=None): self.opener = opener or build_opener(NoRedirect())
    def supports(self, kind): return kind == 'github.create_issue'
    def available(self): return bool(os.environ.get('SOLOOS_GITHUB_TOKEN'))

    def execute(self, action):
        from .actions import validate_action
        validate_action(action)
        if not self.supports(action['kind']) or not self.available():
            raise PermissionError('GitHub issue capability unavailable')
        # Always conservatively classified as a high-risk post, including private repos.
        marker = '\n\n<!-- soloos-idempotency:' + action['idempotency_key'] + ' -->'
        payload = {'title':action['payload']['title'],'body':action['payload']['body']+marker}
        request = Request('https://api.github.com/repos/'+action['target']+'/issues',
                          data=json.dumps(payload).encode('utf-8'), method='POST',
                          headers={'Authorization':'Bearer '+os.environ['SOLOOS_GITHUB_TOKEN'],
                                   'Accept':'application/vnd.github+json','Content-Type':'application/json',
                                   'User-Agent':'SoloOS/1.0', 'X-GitHub-Api-Version':'2022-11-28'})
        with self.opener.open(request, timeout=30) as response:
            if response.status != 201: raise RuntimeError('Unexpected GitHub status')
            raw = response.read(2_000_001)
            if len(raw) > 2_000_000: raise RuntimeError('Response too large')
            result = json.loads(raw)
        if type(result.get('number')) is not int or result['number'] <= 0:
            raise ValueError('Missing issue identifier')
        return {'provider':'github','number':result['number'],
                'url':'https://github.com/'+action['target']+'/issues/'+str(result['number'])}

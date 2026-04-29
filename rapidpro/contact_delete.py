import sys
import csv
from datetime import datetime
from temba.contacts.models import ContactGroup
from temba.users.models import User

TARGET_GROUP_NAME = "deletion request"

def run_gdpr_deletion():
    # 1. Get the admin user for the audit log trail
    admin_user = User.objects.filter(is_superuser=True).first()

    # 2. Find groups across workspaces
    groups = ContactGroup.objects.filter(name__iexact=TARGET_GROUP_NAME, is_active=True)
    if not groups.exists():
        print(f"No active groups named '{TARGET_GROUP_NAME}' found.", file=sys.stderr)
        return

    audit_rows = []
    total_deleted = 0

    # 3. Iterate and Delete
    for group in groups:
        contacts = list(group.contacts.filter(is_active=True))

        for contact in contacts:
            c_uuid = str(contact.uuid)
            c_created = contact.created_on.isoformat()
            org_name = contact.org.name

            try:
                # Triggers native RapidPro hard deletion of contact, messages, runs, and anonymizes URNs
                contact.release(admin_user, immediately=True)
                print(f"[✔] Wiped contact {c_uuid} from workspace '{org_name}'", file=sys.stderr)
                status = "Success"
                total_deleted += 1
            except Exception as e:
                print(f"[!] Failed to wipe {c_uuid}: {e}", file=sys.stderr)
                status = f"Failed: {str(e)}"

            # Append exactly matching our Google Sheet Columns
            audit_rows.append({
                "Workspace": org_name,
                "Anonomous UUID": c_uuid,
                "Request Type": "Deletion",
                "Request Received": c_created,
                "Request Completion": datetime.now().isoformat() if status == "Success" else status,
                "Related emails deleted": "N/A",
                "Partners notified of dataset update": "Pending"
            })

    print(f"\nFinished processing {total_deleted} contacts.", file=sys.stderr)
    print("--------------------------------------------------", file=sys.stderr)

    # 4. Print CSV Report to Standard Out
    if audit_rows:
        writer = csv.DictWriter(sys.stdout, fieldnames=audit_rows[0].keys())
        writer.writeheader()
        writer.writerows(audit_rows)

run_gdpr_deletion()

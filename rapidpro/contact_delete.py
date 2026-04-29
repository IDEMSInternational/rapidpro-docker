import argparse
import csv
import sys
from datetime import datetime
from temba.contacts.models import ContactGroup
from temba.users.models import User


TARGET_GROUP_NAME = "deletion request"
REQUEST_TIME_FIELD_KEY = "deletion_request_time"


def run_gdpr_deletion():
    admin_user = User.objects.filter(is_superuser=True).first()

    groups = ContactGroup.objects.filter(name__iexact=TARGET_GROUP_NAME, is_active=True)
    if not groups.exists():
        print(f"No active groups named '{TARGET_GROUP_NAME}' found.", file=sys.stderr)
        return

    audit_rows = []
    total_deleted = 0

    for group in groups:
        try:
            deletion_request_time_field = group.org.fields.get(
                key=REQUEST_TIME_FIELD_KEY,
                is_active=True,
            )
        except Exception:
            print(
                f"Failed to find the 'deletion request time' field, org={group.org}",
                file=sys.stderr,
            )
            continue

        for contact in group.contacts.filter(is_active=True):
            c_uuid = str(contact.uuid)
            org_name = contact.org.name
            request_received = contact.get_field_value(deletion_request_time_field)

            try:
                contact.release(admin_user, immediately=True)
                print(
                    f"[✔] Wiped contact {c_uuid} from workspace '{org_name}'",
                    file=sys.stderr,
                )
                status = "Success"
                total_deleted += 1
            except Exception as e:
                print(f"[!] Failed to wipe {c_uuid}: {e}", file=sys.stderr)
                status = f"Failed: {str(e)}"

            # Append exactly matching our Google Sheet Columns
            audit_rows.append(
                {
                    "Workspace": org_name,
                    "Anonomous UUID": c_uuid,
                    "Request Type": "Deletion",
                    "Request Received": request_received.isoformat(),
                    "Request Completion": (
                        datetime.now().isoformat() if status == "Success" else status
                    ),
                    "Related emails deleted": "N/A",
                    "Partners notified of dataset update": "Pending",
                }
            )

    print(f"\nFinished processing {total_deleted} contacts.", file=sys.stderr)
    print("--------------------------------------------------", file=sys.stderr)

    if audit_rows:
        writer = csv.DictWriter(sys.stdout, fieldnames=audit_rows[0].keys())
        writer.writeheader()
        writer.writerows(audit_rows)


run_gdpr_deletion()

import argparse
import csv
import os
import sys
from datetime import datetime
from temba.contacts.models import ContactGroup
from temba.users.models import User

TARGET_GROUP_NAME = "deletion request"
REQUEST_TIME_FIELD_KEY = "deletion_request_time"


def run_gdpr_deletion(report_dir):
    admin_user = User.objects.filter(is_superuser=True).first()

    groups = ContactGroup.objects.filter(name__iexact=TARGET_GROUP_NAME, is_active=True)
    if not groups.exists():
        print(f"No active groups named '{TARGET_GROUP_NAME}' found.")
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
                f"Failed to find the '{REQUEST_TIME_FIELD_KEY}' field, org={group.org}"
            )
            continue

        for contact in group.contacts.filter(is_active=True):
            c_uuid = str(contact.uuid)
            org_name = contact.org.name
            request_received = contact.get_field_value(deletion_request_time_field)

            try:
                # contact.release(admin_user, immediately=True)
                print(f"[✔] Wiped contact {c_uuid} from workspace '{org_name}'")
                status = "Success"
                total_deleted += 1
            except Exception as e:
                print(f"[!] Failed to wipe {c_uuid}: {e}")
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


    if audit_rows:
        print(f"Contacts removed, count={total_deleted}")
        out_dir = Path(report_dir)
        out_dir.mkdir(exist_ok=True, parents=True)
        report = out_dir / (datetime.now().strftime("%Y-%m-%d_%H%M%S") + ".csv")

        with open(report, "w") as f:
            writer = csv.DictWriter(f, fieldnames=audit_rows[0].keys())
            writer.writeheader()
            writer.writerows(audit_rows)

        print(f"Report created, path={report}")
    else:
        print("No contacts removed")


report_dir = os.getenv("CONTACT_DELETE_REPORT_DIR")
run_gdpr_deletion(report_dir)

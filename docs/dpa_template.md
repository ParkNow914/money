# Data Processing Addendum (Template)

> Replace bracketed sections with your company/legal entity details before sending to partners.

## 1. Parties

- **Data Controller**: [Client legal name], with registered address [address].
- **Data Processor**: [Your company], with registered address [address].

## 2. Subject matter

Processor provides "always free" monetization infrastructure (IA inference, marketplace, affiliate tracking, datasets) as described in the Master Service Agreement.

## 3. Duration

This DPA remains in effect for as long as Processor handles Personal Data on behalf of Controller.

## 4. Categories of data

- User identifiers (`x-user-id`, email, wallet IDs).
- Marketplace product metadata (title, description, price).
- Payment references (checkout IDs, ledger records—no card data stored).
- KYC attachments (documents uploaded by sellers).

## 5. Data subjects

- End users consuming IA or marketplace content.
- Sellers/partners onboarding through the admin flow.

## 6. Processing instructions

Processor shall:

1. Process data only on documented instructions from Controller.
2. Inform Controller if instructions infringe applicable laws.
3. Ensure confidentiality commitments for employees/contractors.

## 7. Subprocessors

Current list (update when onboarding new vendors):

| Vendor | Purpose | Location |
| --- | --- | --- |
| Amazon Web Services | Hosting (ECS, RDS, S3, CloudWatch) | USA/Brazil (sa-east-1) |
| Hugging Face | IA inference API | USA/EU |
| Sentry | Error monitoring | USA/EU |

Controller must be notified 30 days before adding or replacing a subprocessor.

## 8. Security measures

Processor maintains:

- Encryption in transit (HTTPS/ALB) and at rest (RDS AES-256, S3 SSE).
- Access control via IAM roles with least privilege.
- Network isolation (private subnets for ECS/RDS, security groups for ALB ingress only).
- Monitoring (Sentry, CloudWatch) and audit logging (ledger + invoices).

## 9. Data subject requests

Processor assists Controller via documented APIs (`/api/v1/kyc`, `/api/v1/admin/data/catalog`) or manual exports within 10 business days.

## 10. Breach notification

Processor notifies Controller without undue delay (within 48 hours) after becoming aware of a Personal Data Breach, providing details on scope, impact, and mitigation.

## 11. International transfers

When data leaves Brazil/EU, Processor relies on Standard Contractual Clauses and ensures subprocessors provide adequate safeguards.

## 12. Return or deletion

Upon termination, Processor deletes or returns all Personal Data (at Controller's choice) within 30 days, except where retention is required by law.

---

Controller signature: __________________  Date: ______________

Processor signature: __________________  Date: ______________

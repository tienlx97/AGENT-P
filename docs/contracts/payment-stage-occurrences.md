# PAY-STAGES — agreed additive FE/BE contract

User scope: Logistics → Chi tiết hợp đồng → MỐC ĐIỀU KHOẢN THANH TOÁN.
One agreed payment stage may split into multiple planned payment occurrences.
This extends the contract's payment TERMS; recorded receipts stay in the existing
PaymentSchedules flow. Do not invent paid statuses from the count of receipts.

Keep parent PaymentRatioPercent / PaymentCondition / PaymentType unchanged.
Add optional `PaymentOccurrences` to each contract PaymentTerm request and
`paymentOccurrences` to the corresponding response (normal JSON naming policy).
Each occurrence carries `paymentRatioPercent` (percent OF ITS STAGE),
`paymentCondition` (required, max 200 chars), and `paymentType` (TT/LC).
Occurrences must be 1..20, each percentage >0 and <=100, total 100 with the same
0.01 tolerance as contract payment terms. Omitted/null occurrences on old clients
mean one 100% occurrence using the parent condition/method. An explicit empty
list is invalid. Preserve order as entered. Commission terms remain unchanged.

Example: stage = 30% of a 1000 USD contract; its two occurrences are 40% and 60%:
120 USD + 180 USD = 300 USD. Contract stage percentages still total 100%.
Use the EXISTING Infrastructure HasValueJsonConverter/ValueJsonComparer to store
an additive JSON column on ContractPaymentTerms (no new service or subsystem).
Legacy rows with no column data normalize to one occurrence in Domain/response.
Ship only a new forward migration; do not apply migrations to a live database.

FE reuses PaymentTermsFields, usePaymentTermRows, NumberInput/Selector/TextArea
and existing Meta summary cards. Contract stages can add/remove occurrences while
retaining at least one; show nested ratios, derived stage/occurrence amounts and
validation. Save/create/reload must round trip occurrences. Enable only contract
terms (`hasPaymentType`), preserving commission behavior. Show occurrence details
in the named overview card without marking a stage paid by receipt count.

Test fixture shape:
```json
{"paymentRatioPercent":30,"paymentCondition":"Deposit","paymentType":"TT","paymentOccurrences":[{"paymentRatioPercent":40,"paymentCondition":"First part","paymentType":"TT"},{"paymentRatioPercent":60,"paymentCondition":"Second part","paymentType":"TT"}]}
```

Delivery: separate FE and BE branches/PRs linked by PAY-STAGES, matching-revision
HTTP/integration and UI tests, host-side reviewed commits, no merge or deployment.
BE deploy compatibility proposal for human review: additive BE first, then FE.

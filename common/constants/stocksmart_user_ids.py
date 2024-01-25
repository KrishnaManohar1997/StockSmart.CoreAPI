SS_USER_IDS_PROD = [
    "d82be800-f36c-431a-814a-8b064c7f9441",
    "94d01240-e4f0-4c16-ae3b-c828ca9cb6fb",
    "2ccdbad9-fc94-49cf-b9bb-868c84c2c7a6",
    "69a35f48-c33c-4080-b4f0-d310c3a03620",
    "ebb01321-e75f-4d76-911c-dcc34b6fc241",
    "a0f4e384-9bff-41b8-b27a-ca9919f50f50",
    "81baa5d3-24a4-4ed4-b035-0aee6d0999d0",
    "60d102de-61c9-4576-a3b3-d6f0f5277880",
    "54e625f8-9eae-44c7-93a7-31d668743519",
    "ba93e051-3e3d-4987-b270-a4af3cb2ecf8",
    "4e9cab5e-dcf9-40ba-a211-0ea27fca36b5",
    "2434f863-ca57-4019-b629-1ffd45ad3184",
    "74f07aba-68c8-4b57-91ea-3084e90022f1",
    "fe7b7363-c3c3-441a-a1a2-e7c953baa4a7",
    "ee3480d7-09d3-43c4-9c1f-5f4e2a115a34",
    "95e6895a-fc79-487d-920d-9da25bd7a274",
    "b7ba7160-d36b-4764-a78a-ead41d7975df",
    "3c9f69e9-08e3-4197-af96-8e4934c0b809",
    "bc4f723f-0d03-4289-9319-42f869ed3044",
    "88b2c1ac-d603-49b5-aa1d-90384ff970c1",
    "75209cd2-c2b2-48cd-a37a-aa181623fd87",
    "4094aaa2-fc4b-43ae-8f33-ad9dfe331317",
    "0f6d25eb-a923-4011-b1ee-f9c44283d79b",
]
SS_USER_IDS_DEV = [
    "b1b65b24-84d7-4822-8261-f3b2c73bd0ba",
    "bc71d775-a2ce-4505-bd40-c0a2d4408a83",
    "3032f897-853f-4eec-bbb2-022d249e5764",
    "f7ec30cf-fcfa-4927-a105-8a0cb9462eae",
    "b3260bc7-a3fa-4754-aa2e-5ec3b0408803",
    "95eae917-695b-4628-8109-d48cd1724ecc",
    "13b55147-2ceb-45f7-b9a8-f6b9a84f1638",
    "84a748b4-4491-490c-99de-6d6177f4863a",
    "38279a31-d8e7-409d-a63c-dadcf9986477",
    "51d7ebd2-20f5-4fea-ab31-307731759909",
    "352d3f7e-ba57-4fc2-bae0-61eeb2246a01",
    "b7cd9dec-9c42-4e50-9df0-d70cff3c1e9f",
    "51e03ca7-490b-4807-a301-c499196247ad",
    "d1fa8f3c-e687-4519-80dc-6e7573f3d22f",
    "240fa625-b522-42f9-a31c-3c8287c543b2",
    "1c3666d2-b3fe-4afb-8df5-8b7d853b0c20",
]


def get_ss_user_ids(env="PRODUCTION"):
    if env == "PRODUCTION":
        return SS_USER_IDS_PROD
    return SS_USER_IDS_DEV

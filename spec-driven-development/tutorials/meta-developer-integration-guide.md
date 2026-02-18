# Meta Official Integration Guide (Facebook + Instagram + WhatsApp)

Last updated: 2026-02-18

## 0. Important Rule Before You Start

1. You can use GET for reading data (IDs, account linkage, token validation, metadata).
2. You cannot use GET for publishing actions.
3. Facebook posting, Instagram publishing, and WhatsApp sending require POST by Meta API design.
4. If you call those endpoints with GET, Meta returns an error like "Unsupported get request".

So in this guide:
1. All read/lookup commands are GET.
2. Action calls are POST (required).

---

## 1. What You Can and Cannot Do via Official Meta APIs

Supported:
1. Post to Facebook Page (not personal profile).
2. Publish to Instagram Professional account (Business/Creator), linked correctly.
3. Send WhatsApp messages via WhatsApp Cloud API.

Not supported:
1. Posting to personal Facebook timeline/profile with official Graph API.

---

## 2. Accounts and Access Checklist (Do This First)

1. Facebook account with admin or equivalent task permissions on target Facebook Page.
2. Instagram account switched to Professional (Business or Creator).
3. Instagram account linked to the same Facebook Page.
4. Meta developer account.
5. Meta Business Portfolio (Business Manager).
6. For WhatsApp:
   - WhatsApp Business Account (WABA)
   - A phone number in WhatsApp API Setup (test or production)

---

## 3. Create the Meta App (One App for Facebook + Instagram + WhatsApp)

Where to do this:
1. Open browser -> `https://developers.facebook.com/apps`

Steps:
1. Click `Create App`.
2. Choose app type for business integrations (Business flow in current UI).
3. Fill app name, contact email, business portfolio.
4. Click create.
5. In app dashboard left menu, click `Add Product`.
6. Add:
   - Facebook Login for Business (or Facebook Login if that is what UI shows)
   - Instagram API
   - WhatsApp

---

## 4. Graph API Explorer: Exactly Where to Run GET Requests

Where to open:
1. `https://developers.facebook.com/tools/explorer/`
2. Or Meta app dashboard -> `Tools` -> `Graph API Explorer`.

In the Explorer UI, use these controls:
1. App selector dropdown (top area): choose your app.
2. Access token area: generate/select token.
3. HTTP method dropdown (left of endpoint): select GET or POST.
4. Endpoint input box (center): e.g. `/me/accounts`.
5. Params panel: add query params like `fields`.
6. Click `Submit`.
7. Copy values from JSON response panel.

---

## 5. Facebook First (Main Path)

### 5.1 Generate User Access Token (Explorer UI)

In Graph API Explorer:
1. Select your app.
2. Click token dropdown/button to generate User Access Token.
3. Add permissions:
   - `pages_show_list`
   - `pages_manage_posts`
   - `pages_read_engagement` (some UIs show `pages_manage_read_engagement`)
4. If you also want Instagram in same token flow, also add:
   - `instagram_basic`
   - `instagram_content_publish`
5. Complete login/consent popup.

Result:
1. Explorer now has a user token in the token field.

### 5.2 GET the Page List and Page Tokens

Where to run:
1. Graph API Explorer
2. Method: GET
3. Endpoint: `me/accounts`
4. Params: none required
5. Click `Submit`

Expected response:
1. JSON with `data[]`
2. For each page entry, look for:
   - `id` (Page ID)
   - `name`
   - `access_token` (Page token)
   - `tasks`

Copy these for target page:
1. `FACEBOOK_PAGE_ID=<id>`
2. `FACEBOOK_PAGE_TOKEN=<access_token>`

Equivalent terminal GET command:

```bash
curl -G "https://graph.facebook.com/v24.0/me/accounts" \
  --data-urlencode "access_token=<USER_ACCESS_TOKEN>"
```

### 5.3 GET Page Basic Info (Sanity Check)

Where to run:
1. Graph API Explorer
2. Method: GET
3. Endpoint: `/<FACEBOOK_PAGE_ID>`
4. Params:
   - `fields=id,name`
5. Click `Submit`

Expected:
1. Response contains exact page id and page name.

Equivalent terminal GET command:

```bash
curl -G "https://graph.facebook.com/v24.0/<FACEBOOK_PAGE_ID>" \
  --data-urlencode "fields=id,name" \
  --data-urlencode "access_token=<FACEBOOK_PAGE_TOKEN>"
```

### 5.4 POST a Real Facebook Test Post (Required POST)

Why POST:
1. `/{page-id}/feed` creates content. Graph API requires POST.

Where to run in Explorer:
1. Method: POST
2. Endpoint: `/<FACEBOOK_PAGE_ID>/feed`
3. Body params:
   - `message=Facebook integration live test`
4. Token: use `FACEBOOK_PAGE_TOKEN`
5. Click `Submit`

Expected:
1. Response contains post id.

Equivalent terminal command (POST, not GET):

```bash
curl -X POST "https://graph.facebook.com/v24.0/<FACEBOOK_PAGE_ID>/feed" \
  -d "message=Facebook integration live test" \
  -d "access_token=<FACEBOOK_PAGE_TOKEN>"
```

### 5.5 Put Facebook Values in `.env`

```env
FACEBOOK_POST_METHOD=graph_api
FACEBOOK_PAGE_ID=
FACEBOOK_PAGE_TOKEN=
```

---

## 6. Instagram Setup

Instagram depends on correct Facebook Page linkage.

### 6.1 Confirm Instagram Professional + Link to Page

Where to do this:
1. Instagram app (mobile): switch to Professional account.
2. Facebook Page settings: linked accounts -> Instagram.
3. Ensure the exact Instagram account is connected to the exact page from section 5.

### 6.2 GET Instagram Business Account ID via Page

Where to run:
1. Graph API Explorer
2. Method: GET
3. Endpoint: `/<FACEBOOK_PAGE_ID>`
4. Params:
   - `fields=instagram_business_account{id,username}`
5. Token: `FACEBOOK_PAGE_TOKEN`
6. Click `Submit`

Expected:
1. Response includes `instagram_business_account` object.
2. Copy `instagram_business_account.id` as:
   - `INSTAGRAM_BUSINESS_ID`

Equivalent terminal GET command:

```bash
curl -G "https://graph.facebook.com/v24.0/<FACEBOOK_PAGE_ID>" \
  --data-urlencode "fields=instagram_business_account{id,username}" \
  --data-urlencode "access_token=<FACEBOOK_PAGE_TOKEN>"
```

### 6.3 Token Choice for This Repo

In this repository's supported flow:
1. `INSTAGRAM_ACCESS_TOKEN` is commonly the same as page token.
2. Set:
   - `INSTAGRAM_ACCESS_TOKEN=<FACEBOOK_PAGE_TOKEN>`

### 6.4 GET Instagram Account Basic Data (Sanity Check)

Where to run:
1. Graph API Explorer
2. Method: GET
3. Endpoint: `/<INSTAGRAM_BUSINESS_ID>`
4. Params:
   - `fields=id,username,name,media_count`
5. Token: `INSTAGRAM_ACCESS_TOKEN`
6. Click `Submit`

Equivalent terminal GET command:

```bash
curl -G "https://graph.facebook.com/v24.0/<INSTAGRAM_BUSINESS_ID>" \
  --data-urlencode "fields=id,username,name,media_count" \
  --data-urlencode "access_token=<INSTAGRAM_ACCESS_TOKEN>"
```

### 6.5 Instagram Publish Flow (Required POST)

This is 3-step and action endpoints are POST by design.

Step A: create media container (POST)
1. Explorer method: POST
2. Endpoint: `/<INSTAGRAM_BUSINESS_ID>/media`
3. Params:
   - `image_url=<public_https_image_url>`
   - `caption=<your_caption>`
4. Submit and copy container id from response (`id`).

Step B: poll container status (GET)
1. Explorer method: GET
2. Endpoint: `/<CONTAINER_ID>`
3. Params:
   - `fields=status_code`
4. Wait until `status_code=FINISHED`.

Step C: publish container (POST)
1. Explorer method: POST
2. Endpoint: `/<INSTAGRAM_BUSINESS_ID>/media_publish`
3. Params:
   - `creation_id=<CONTAINER_ID>`
4. Submit.
5. Response returns published media id.

### 6.6 Put Instagram Values in `.env`

```env
INSTAGRAM_POST_METHOD=graph_api
INSTAGRAM_BUSINESS_ID=
INSTAGRAM_ACCESS_TOKEN=
```

---

## 7. WhatsApp Cloud API Setup

### 7.1 Get Values from Meta App -> WhatsApp -> API Setup

Where to do this:
1. Meta app dashboard -> `WhatsApp` -> `API Setup`

Copy:
1. Access token (temporary for quick tests or permanent system user token for stable use).
2. Phone Number ID.
3. Optional additional identifiers shown in UI (WABA ID, etc.) for your records.

Set:
1. `WHATSAPP_ACCESS_TOKEN`
2. `WHATSAPP_PHONE_NUMBER_ID`

### 7.2 (Recommended) Create Permanent System User Token

Where:
1. `https://business.facebook.com/settings`

Steps:
1. Users -> System Users -> Add.
2. Assign assets (app + WhatsApp assets).
3. Generate token with:
   - `whatsapp_business_messaging`
   - `whatsapp_business_management`
   - `business_management` if required in your flow
4. Replace temporary token with this permanent token in `.env`.

### 7.3 Configure Webhook (Exact Matching Token)

Where:
1. App dashboard -> WhatsApp -> Configuration/Webhooks

Set:
1. Callback URL: `https://<your-public-domain>/api/webhooks/whatsapp`
2. Verify token: choose random secret string
3. Subscribe to `messages` field

Critical:
1. Meta UI verify token and `.env` `WHATSAPP_VERIFY_TOKEN` must be exactly identical.

This repo endpoint handling:
1. `dashboard/src/app/api/webhooks/whatsapp/route.ts`

### 7.4 WhatsApp Send Test (Required POST)

Why POST:
1. `/{phone-number-id}/messages` sends a message, so it is write/action endpoint.

Explorer run:
1. Method: POST
2. Endpoint: `/<WHATSAPP_PHONE_NUMBER_ID>/messages`
3. JSON body:
   - `messaging_product=whatsapp`
   - `to=<E164_NUMBER>`
   - `type=template`
   - `template.name=hello_world`
   - `template.language.code=en_US`
4. Submit.

Equivalent terminal command (POST, not GET):

```bash
curl -X POST "https://graph.facebook.com/v24.0/<WHATSAPP_PHONE_NUMBER_ID>/messages" \
  -H "Authorization: Bearer <WHATSAPP_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d "{\"messaging_product\":\"whatsapp\",\"to\":\"<E164_NUMBER>\",\"type\":\"template\",\"template\":{\"name\":\"hello_world\",\"language\":{\"code\":\"en_US\"}}}"
```

---

## 8. Exact `.env` Mapping

```env
META_GRAPH_API_VERSION=v24.0
WHATSAPP_API_VERSION=v24.0

FACEBOOK_POST_METHOD=graph_api
INSTAGRAM_POST_METHOD=graph_api

FACEBOOK_PAGE_ID=
FACEBOOK_PAGE_TOKEN=

INSTAGRAM_BUSINESS_ID=
INSTAGRAM_ACCESS_TOKEN=

WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_VERIFY_TOKEN=choose-a-random-secret-string
WHATSAPP_WEBHOOK_DOMAIN=personal
```

Important:
1. Keep one value per key in `.env` (no duplicates).
2. Keep `META_GRAPH_API_VERSION` and `WHATSAPP_API_VERSION` aligned unless you intentionally need split versions.

---

## 9. Value-by-Value: Where Exactly Each Key Comes From

1. `FACEBOOK_PAGE_ID`
   - Source: GET `/me/accounts` response -> target page entry -> `id`
2. `FACEBOOK_PAGE_TOKEN`
   - Source: GET `/me/accounts` response -> target page entry -> `access_token`
3. `INSTAGRAM_BUSINESS_ID`
   - Source: GET `/<FACEBOOK_PAGE_ID>?fields=instagram_business_account{id,username}` -> `instagram_business_account.id`
4. `INSTAGRAM_ACCESS_TOKEN`
   - Source: usually same token value as `FACEBOOK_PAGE_TOKEN` in this integration flow
5. `WHATSAPP_ACCESS_TOKEN`
   - Source: WhatsApp API Setup temporary token, or Business Settings generated system user token
6. `WHATSAPP_PHONE_NUMBER_ID`
   - Source: WhatsApp API Setup panel
7. `WHATSAPP_VERIFY_TOKEN`
   - Source: you create it manually; must match exactly between Meta webhook UI and local `.env`
8. `META_GRAPH_API_VERSION`
   - Source: set manually to version you are targeting (this guide uses `v24.0`)
9. `WHATSAPP_API_VERSION`
   - Source: usually same as `META_GRAPH_API_VERSION`

---

## 10. Troubleshooting (Common Real Failures)

1. Facebook post fails with permissions error:
   - Regenerate token with page permissions.
   - Confirm your user has required page tasks (e.g., create content).
2. `instagram_business_account` is null:
   - IG is not linked to the exact page.
   - IG account is not Professional.
3. Instagram container stuck or error:
   - `image_url` not public HTTPS.
   - Media format invalid.
4. WhatsApp accepted response but no delivery on phone:
   - Recipient not configured correctly for test mode.
   - Conversation/template constraints.
   - Number not in proper E.164 format.
5. Webhook verification fails:
   - verify token mismatch between Meta UI and `.env`
   - callback URL not publicly reachable over HTTPS

---

## Official Source Links

1. Access Token Guide (Facebook Login): `https://developers.facebook.com/docs/facebook-login/guides/access-tokens/`
2. Instagram API with Facebook Login for Business (Get Started): `https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/get-started/`
3. Instagram Platform overview: `https://developers.facebook.com/docs/instagram-platform/`
4. Facebook Pages API prerequisites: `https://developers.facebook.com/docs/page-stories-api`
5. WhatsApp Cloud API docs: `https://developers.facebook.com/docs/whatsapp/`
6. Webhook verification contract: `https://developers.facebook.com/docs/admin-center/webhooks`
7. Graph API changelog: `https://developers.facebook.com/docs/graph-api/changelog/versions/`

Made with precision by DanielCodeForge 💖

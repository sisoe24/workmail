# Workmail

Minimal clock in / clock out email sender for CLI, Raycast, and iPhone.

## Environment

Serverless endpoint:

- `WORKMAIL_SECRET`
- `WORKMAIL_RECEIVER`
- `RESEND_API_KEY`
- `WORKMAIL_FROM_EMAIL`

CLI:

- `WORKMAIL_API_URL`
- `WORKMAIL_SECRET`
- `WORKMAIL_RECEIVER` for `--dry-run`

## Local usage

Dry run:

```bash
WORKMAIL_RECEIVER="manager@example.com" python3 main.py in --dry-run
```

Send through the hosted endpoint:

```bash
WORKMAIL_API_URL="https://your-app.vercel.app/api/clock" \
WORKMAIL_SECRET="replace-me" \
python3 main.py in
```

## Vercel deployment

1. Create a Vercel project from this directory.
2. Add the endpoint environment variables in Vercel:
   - `WORKMAIL_SECRET`
   - `WORKMAIL_RECEIVER`
   - `RESEND_API_KEY`
   - `WORKMAIL_FROM_EMAIL`
3. Deploy. Vercel will expose the Python function and route `/api/clock` to it.

The endpoint only accepts:

```http
POST /api/clock
Authorization: Bearer <WORKMAIL_SECRET>
Content-Type: application/json

{"action":"in"}
```

## Raycast

Create two Script Commands.

Clock in:

```bash
#!/bin/bash
curl -sS \
  -X POST "https://your-app.vercel.app/api/clock" \
  -H "Authorization: Bearer YOUR_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"action":"in"}'
```

Clock out:

```bash
#!/bin/bash
curl -sS \
  -X POST "https://your-app.vercel.app/api/clock" \
  -H "Authorization: Bearer YOUR_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"action":"out"}'
```

## iPhone Shortcuts

Create two shortcuts with:

1. `Get Contents of URL`
2. Method: `POST`
3. URL: `https://your-app.vercel.app/api/clock`
4. Headers:
   - `Authorization: Bearer YOUR_SECRET`
   - `Content-Type: application/json`
5. JSON body:
   - clock in: `{"action":"in"}`
   - clock out: `{"action":"out"}`

This works from mobile data because the endpoint is internet-hosted.

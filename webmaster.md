# Curl commands

## Check HTTP headers and redirects from outside (internet):
```bash
curl -I http://linux.peaberry.cloud
```
## Follow redirects and show headers for HTTPS (to debug SSL connectivity):
```bash
curl -IL https://linux.peaberry.cloud
```

## Verbose curl to a Docker network hostname to check response and headers:
```bash
curl -v http://peaberry/
```

# OpenSSL commands

## Inspect the certificate details and DNS names (to verify domains in the cert):
```bash
openssl x509 -in /full/path/to/certificates/live/peaberry.cloud/fullchain.pem -noout -text | grep DNS:
```


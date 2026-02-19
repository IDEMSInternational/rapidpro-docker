FROM golang:1.24 AS builder
ARG TAG=v10.2.0
WORKDIR /src
RUN git clone --depth=1 --branch=${TAG} https://github.com/nyaruka/rp-indexer.git .
RUN CGO_ENABLED=0 go build -a -o /bin/rp-indexer github.com/nyaruka/rp-indexer/v10/cmd/rp-indexer

FROM scratch
ENV PATH=/bin
COPY --from=builder /bin/rp-indexer /bin/
COPY --from=alpine:3.23.3 /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
CMD ["rp-indexer"]

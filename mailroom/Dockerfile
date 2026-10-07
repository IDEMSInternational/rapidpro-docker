FROM golang:1.26 AS builder
ARG TAG=v26.2.0
WORKDIR /go/src
RUN git clone --depth=1 --branch=${TAG} https://github.com/nyaruka/mailroom.git .
RUN CGO_ENABLED=0 go build -tags timetzdata -a -o /go/bin/ ./cmd/mailroom ./cmd/mrindex
RUN curl -sSL "https://github.com/nyaruka/goflow/releases/download/$(grep goflow go.mod | awk '{print $2}')/docs.tar.gz" | tar -xzf - -C /

FROM scratch
ENV PATH=/bin
COPY --from=builder /go/bin/mailroom /go/bin/mrindex /bin/
COPY --from=builder /docs /docs
COPY --from=alpine:3.23.3 /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
CMD ["mailroom"]

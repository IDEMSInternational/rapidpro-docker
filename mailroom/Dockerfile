FROM golang:1.24 AS builder
ARG TAG=v10.2.0
WORKDIR /go/src
RUN git clone --depth=1 --branch=${TAG} https://github.com/nyaruka/mailroom.git .
RUN CGO_ENABLED=0 go build -tags timetzdata -a -o /go/bin/mailroom github.com/nyaruka/mailroom/cmd/mailroom

FROM golang:1.24 AS docs
WORKDIR /go/src
RUN apt update && apt install -y --no-install-recommends pandoc gettext
COPY --from=builder /go/src/go.mod /tmp/go.mod
RUN git clone --depth=1 --branch $(grep goflow /tmp/go.mod | cut -d" " -f2) https://github.com/nyaruka/goflow.git .
RUN go install github.com/nyaruka/goflow/cmd/docgen && docgen

FROM scratch
ENV PATH=/bin
COPY --from=builder /go/bin/mailroom /bin/
COPY --from=docs /go/src/docs/en-us /docs
COPY --from=alpine:3.23.3 /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
CMD ["mailroom"]

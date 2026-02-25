FROM golang:1.24 AS builder
ARG TAG=v10.2.0
WORKDIR /go/src
RUN git clone --depth=1 --branch=${TAG} https://github.com/nyaruka/courier.git .
RUN CGO_ENABLED=0 go build -tags timetzdata -a -o /go/bin/courier github.com/nyaruka/courier/cmd/courier

FROM scratch
ENV PATH=/bin
COPY --from=builder /go/bin/courier /bin/
COPY --from=alpine:3.23.3 /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
CMD ["courier"]

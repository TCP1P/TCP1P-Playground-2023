<?php

class JWT
{
    private string $passphrase;
    private string $cipher_algo;

    public function __construct($passphrase)
    {
        $this->passphrase = $passphrase;
        $this->cipher_algo = 'aes-128-gcm';
    }

    public function encode($data): string
    {
        $iv = random_bytes(12);
        $header = json_encode(['alg' => 'AES-128-GCM', 'typ' => 'JWT', 'iv' => base64_encode($iv)]);
        $payload = json_encode($data);
        $cipherText = openssl_encrypt($payload, $this->cipher_algo, $this->passphrase, 0, $iv, $tag);
        return base64_encode($header) .'.'. $cipherText .'.'. base64_encode($tag);
    }
    public function decode($jwtToken): array
    {
        list($encodedHeader, $encodedCipherText, $encodedTag) = explode('.', $jwtToken);
        $header = json_decode(base64_decode($encodedHeader), true);
        $iv = base64_decode($header['iv']);
        $tag = base64_decode($encodedTag);
        $payload = openssl_decrypt($encodedCipherText, $this->cipher_algo, $this->passphrase, 0, $iv, $tag);
        return json_decode($payload, true);
    }
}

$jwt = new JWT("testing");

var_dump(json_encode(["role"=>"guest"]));

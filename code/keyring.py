import keyring

keyring.set_password('dart_api_key', 'Henry', '7ff0e503663bfbef8f21c727dec9d2941198ce96')
keyring.set_password('slack_token', 'Henry', 'xoxb-3201556049680-3232837627973-fvhWHIWoNkJMMdgcmNvtHaMi')
keyring.set_password('mock_app_key', 'Henry', 'PSEC6mDNKVxSpSiftSPPnXVBZY1QcQPXltqx')
keyring.set_password('mock_app_secret', 'Henry', 'dPQsP1h6zvODlbsbHz0J4Sz2oOe9Nmb413UiD3WU0aQ4pUa4CVAUzUrcHPtHysUePiALo6R8W13s/EWEaN05pL7TcQr7lyVTYElGiA5Ws4GOZasPCIPpHDBQRF6RdhUdx9DshUuFIDdwLeM+cfjdXuss/qxc5qD1SbwFn94CvRuaMhcE9xc=')

keyring.set_password('real_app_key', 'Henry', 'PSeXhE4AnaMgNU4w3wd1TNTOc8Xc1TPfOStf')
keyring.set_password('real_app_secret', 'Henry', '0galoTKttmS3PZ5358I3yg+4cf/fpfWF98dVKyKWjDZim9x2CjantLKNj5cJPT/H78D+K3zQ31cbD49rj6VZYgQcVV9I2lzDRpjAvkUAsVSYRm7GfYI9RsBv6lZ5+LPJOWZZYuneUvtb+81h5mnhlxzU67q+5Lfp5r3SFbuY0OSegou1p1A=')


keyring.get_password('dart_api_key', 'Henry')
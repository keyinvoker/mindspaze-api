upstream mindspaze_api {
    server unix:/srv/mindspaze/uwsgi/mindspaze.sock;
}

server {
    client_max_body_size 100M;

    # SSL
    # listen 443 ssl;
    # ssl_protocols TLSv1.3;
    # ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH';
    # ssl_prefer_server_ciphers on;
    # ssl_certificate /etc/ssl/certs/devcloud1.pem;
    # ssl_certificate_key /etc/ssl/private/devcloud1.key;
    # ssl_session_cache shared:SSL:20m; ssl_session_timeout 180m;

    location / {
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Credentials' 'true' always;
        add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type, Authorization, Origin' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE' always;
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain charset=UTF-8';
            add_header 'Content-Length' 0;
            add_header 'Access-Control-Allow-Credentials' 'true';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE';
            add_header 'Access-Control-Allow-Origin' *;
            add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type, Authorization, Origin';
            return 204;
        }

        rewrite  ^/api/mindspaze/(.*) /$1 break;
        #uwsgi_param SCRIPT_NAME /api/mindspaze;
        #include     uwsgi_params;
        #uwsgi_pass   mindspaze_api;
        #uwsgi_read_timeout         60;

        proxy_pass http://127.0.0.1:5000;
        #proxy_connect_timeout      60s;
        #proxy_send_timeout         60s;
        #proxy_read_timeout         60s;
    }
}

server {
    listen 80;
    return 301;
}
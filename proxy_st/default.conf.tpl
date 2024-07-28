server {
    listen 80;
    server_name www.example.com;  # 수정 필요!!!

    location /app1 {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /app2 {
        proxy_pass http://localhost:8502;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /app3 {
        proxy_pass http://localhost:8503;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
FROM nginx:1.14.2-alpine
COPY . /usr/share/nginx/html
EXPOSE 80
CMD ["nginx","-g","daemon off;"]
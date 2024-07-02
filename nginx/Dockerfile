# Use the official Nginx image as the base image
FROM nginx

# Copy the custom Nginx configuration file into the container
COPY ./nginx.conf /tmp/nginx.conf

# Set environment variables
ENV FLASK_SERVER_ADDR=flask:9090

# Install bash and gettext for envsubst, then clean up apt cache to keep the image size down
RUN apt-get update && \
    apt-get install -y bash gettext-base && \
    rm -rf /var/lib/apt/lists/*

# Use envsubst to replace environment variables in nginx.conf and move it to the final location
CMD /bin/bash -c "envsubst < /tmp/nginx.conf > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"
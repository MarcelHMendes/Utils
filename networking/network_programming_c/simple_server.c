#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include "network.h"
#include <unistd.h>

#define PORT 7990

int main(void){
    int sockfd, new_sockfd; //listen on sock_fd, new connection on new_fd
    struct sockaddr_in host_addr, client_addr;
    struct in_addr inaddr;
    socklen_t sin_size;
    int recv_length = 1;
    int yes = 1;

    char buffer[1024];

    if ((sockfd = socket(PF_INET, SOCK_STREAM, 0)) == -1){   //Init socket        
        perror("in socket");
        exit(1);
    }
    
    if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) == -1){
        perror("setting socket option SO_REUSEADDR");
        exit(1);
    }
    
    if(inet_pton(AF_INET,"127.0.0.1",&inaddr) == -1){
        perror("inet_pton");
        exit(1);
    }

    host_addr.sin_family = AF_INET; //host byteorder
    host_addr.sin_port = htons(PORT); //short, network byte order
    host_addr.sin_addr = inaddr; 
    //memset(&(host_addr.sin_zero), '\0', 8);

    if (bind(sockfd, (struct sockaddr *) &host_addr, sizeof(struct sockaddr)) == -1){
        perror("biding on socket");
        exit(1);
    }

    if (listen(sockfd, 5) == -1){
        perror("listening on socket");
        exit(1);
    }

    while(1){ //Accept loop
        sin_size = sizeof(struct sockaddr_in);
        new_sockfd = accept(sockfd, (struct sockaddr *) &client_addr, &sin_size);
        if (new_sockfd == -1)
            perror("accepting connection");
        printf("server got connection from %s port %d", inet_ntoa(client_addr.sin_addr),
                ntohs(client_addr.sin_port));
        send(new_sockfd, "Hello World\n", 13, 0);
        recv_length = recv(new_sockfd, &buffer, 1024, 0);
        while(recv_length > 0){
            printf("received %d bytes\n", recv_length);
            dump((const unsigned char *) buffer, recv_length);
            recv_length = recv(new_sockfd, &buffer, 1024, 0);
        }
        close(new_sockfd);
    }
    
    return 0; 
}

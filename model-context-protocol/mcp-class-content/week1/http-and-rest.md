# HTTP and REST #1

## HTTP:

Hmm, The full form of HTTP is Hypertext Transfer Protocol, It's the fundamental client-server communication protocol of the web, every single interaction involves two main parts. first is the request sent by the client contains a method like GET, POST and DELETE, a URL, headers and sometimes a body, the second part is the response sent by the server to the client, containing a status code like 200 for success or 404 for not found, the response can also contains headers and body.

## REST:

So! The full form of REST is Representational State Transfer, It's actually an architectural style built on top of HTTP, and it introduces a few key principles like resources identified by a URL, like /users/42 is a resource, and statelessness means every single request from the client to the server must contain all the information the server needs to fulfil the request, REST APIs use JSON as the standard format for sending and receiving data.

## Exercise:

Let's say we are designing a REST API for a books library, this is how it will looks like.

1. To get a specific book: GET /books/book-id

2. To add a new book: POST /books -- because book details will go inside the body formatted as JSON

3. To delete a book: DELETE /books/book-id

4. NOTE: /books is a collection of resource, /books/book-id is a single resource

5. The methods are part of HTTP and principles are for REST

6. No verbs in URL mean No /getBooks, No /deleteBook

Good Luck 👋🏻
const prod = {
    serverDomain: 'server-h3j5wl475a-as.a.run.app',
    httpProtocol: 'https',
    webSocketProtocol: 'wss'
}

const dev = {
    serverDomain: 'localhost:8000',
    httpProtocol: 'http',
    webSocketProtocol: 'ws'
}

export const config = process.env.NODE_ENV === 'development' ? dev : prod;
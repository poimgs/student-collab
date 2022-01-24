import Alert from '@mui/material/Alert';

const WebsocketWarning = () => {
    return (
        <Alert severity="error" sx={{ margin: 1 }}>
            You have disconnected from the server, please refresh to continue cheati- collaborating with peers!
        </Alert>
    )
}

export default WebsocketWarning;
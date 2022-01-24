import { Typography } from '@mui/material';
import Grid from '@mui/material/Grid';

const NotAuthorized = () => {
    return (
        <Grid container direction="column" alignItems="center" mt={'15%'}>
            <Typography variant="h3">
                You are not authorized to view this page
            </Typography>
            <Typography variant="h4" mt={4}>
                Wait... how did you even know about this link?
            </Typography>
            <Typography variant="h5" mt={4}>
                Please don't hack me!
            </Typography>
            <Typography variant="p" mt={4}>
                Pleeeeeeeeeeeeeease
            </Typography>
        </Grid >
    )
}

export default NotAuthorized;
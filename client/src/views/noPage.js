import { Typography } from '@mui/material';
import Grid from '@mui/material/Grid';
import NavBar from '../components/navBar';

const NoPage = () => {
    return (
        <>
            <NavBar />
            <Grid container direction="column" alignItems="center" mt={'23%'}>
                <Typography variant="h3">
                    Nothing to see here! 404!
                </Typography>
            </Grid >
        </>
    )
}

export default NoPage;
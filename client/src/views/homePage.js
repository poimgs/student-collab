import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import QuestionAnswerIcon from '@mui/icons-material/QuestionAnswer';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import NavBar from '../components/navBar';
import { checkAuthenticated } from '../helpers/auth';

const Home = () => {
    // const auth = useContext(AuthContext)
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        const isAuthenticated = checkAuthenticated();
        if (!isAuthenticated) {
            navigate('/signIn', {
                state: {
                    from: location.pathname
                }
            });
        }
    }, []);

    return (
        <>
            <NavBar />
            <Grid container direction="column" alignItems="center" mt={'20%'}>
                <Typography variant="h3">
                    StackOverflow for Students by Students <QuestionAnswerIcon fontSize="large" />
                </Typography>
                <Typography>
                    Not much to see here for now, but you can access your rooms on the top right hand corner!
                </Typography>
            </Grid >
        </>
    )
}

export default Home;
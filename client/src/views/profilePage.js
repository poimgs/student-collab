import QuestionAnswerIcon from '@mui/icons-material/QuestionAnswer';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import NavBar from '../components/navBar';

const ProfilePage = () => {
    return (
        <Box>
            <NavBar />
            <Grid container direction="column" alignItems="center" mt={'20%'}>
                <Typography variant="h3">
                    StackOverflow for Students by Students <QuestionAnswerIcon fontSize="large" />
                </Typography>
                <Typography>
                    Stuff are still pretty messy at the moment, but this is will be your profile page!
                </Typography>
                <Typography>
                    Thinking of putting stuff like whether you wanna be anonymous and details of which rooms/modules you have access to... but for now, it's just empty
                </Typography>
            </Grid >
        </Box>
    )
}

export default ProfilePage;
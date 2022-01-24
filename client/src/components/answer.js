// import Grid from '@mui/material/Grid'
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Divider from '@mui/material/Divider';
// import Badge from '@mui/material/Badge';
// import IconButton from '@mui/material/IconButton';
// import ThumbUpOffAltIcon from '@mui/icons-material/ThumbUpOffAlt';
// import ThumbUpAltIcon from '@mui/icons-material/ThumbUpAlt';

const Answer = ({ answer }) => {
    // const onUpvoteButtonClick = () => {

    // }
    // const upvotes = 5;
    // const upvoted = true;

    return (
        <Container>
            <AccordionDetails>
                {/* <Grid container spacing={2}>
                    <Grid item xs={11}> */}
                <Typography style={{ whiteSpace: 'pre-line' }}> {answer}</Typography>
                {/* </Grid>
                    <Grid item xs={1}>
                        <IconButton
                            onClick={onUpvoteButtonClick}
                            sx={{ flex: 1 }}
                        >
                            <Badge
                                badgeContent={upvotes}
                                color="info"
                            >
                                {upvoted ? <ThumbUpAltIcon color='info' /> : <ThumbUpOffAltIcon />}
                            </Badge>
                        </IconButton>
                    </Grid>
                </Grid> */}

            </AccordionDetails>
            <Divider />
        </Container >
    );
}

export default Answer;
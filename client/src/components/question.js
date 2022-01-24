import { makeStyles } from "@material-ui/core/styles";
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import Typography from '@mui/material/Typography';
import Badge from '@mui/material/Badge';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import IconButton from '@mui/material/IconButton';
import ThumbUpOffAltIcon from '@mui/icons-material/ThumbUpOffAlt';
import ThumbUpAltIcon from '@mui/icons-material/ThumbUpAlt';
import Answer from './answer';
import AnswerInput from './answerInput';
import { useState } from 'react';

const useStyles = makeStyles(theme => ({
    root: {
        width: "100%",
        "& .MuiAccordionSummary-root:hover": {
            cursor: "default"
        }
    },
}));

const Question = ({ questionInfo, handleAnswerInputEnter, handleQuestionUpvoteButtonClick }) => {
    const classes = useStyles();
    const question = questionInfo.question;
    const upvoted = questionInfo.upvoted;
    const upvotes = questionInfo.upvotes;
    const question_id = questionInfo.id;
    const answers = questionInfo.answers;
    const numAnswers = answers.length.toString();

    const [expand, setExpand] = useState(false);
    const [expanded, setExpanded] = useState(false);

    const toggleAccordian = () => {
        setExpand(!expand);
        setExpanded(!expanded);
    }

    const onUpvoteButtonClick = () => {
        handleQuestionUpvoteButtonClick(question_id, !upvoted);
    }

    return (
        <Accordion expanded={expand} className={classes.root}>
            <AccordionSummary
                expandIcon={
                    <IconButton onClick={toggleAccordian}>
                        <Badge badgeContent={expanded ? null : numAnswers} color="primary">
                            <ExpandMoreIcon />
                        </Badge>
                    </IconButton>
                }
                sx={{ ":hover": { cursor: 'default' } }}
            >
                <Typography my={'auto'}>Q: {question}</Typography>
                <IconButton
                    sx={{ ml: 'auto' }}
                    onClick={onUpvoteButtonClick}
                >
                    <Badge
                        badgeContent={upvotes}
                        color="primary"
                    >
                        {upvoted ? <ThumbUpAltIcon color='primary' /> : <ThumbUpOffAltIcon />}
                    </Badge>
                </IconButton>
            </AccordionSummary>
            {answers.map((answer) => {
                return (
                    <Answer
                        key={answer.id}
                        answer={answer.answer}
                    />
                )
            })}
            <AnswerInput
                question_id={question_id}
                handleAnswerInputEnter={handleAnswerInputEnter}
            />
        </Accordion >
    );
}

export default Question;
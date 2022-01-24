import axios from 'axios';
import { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import NavBar from '../components/navBar';
import ModuleHeader from '../components/moduleHeader';
import QuestionInput from '../components/questionInput';
import Questions from '../components/questions';
import WebsocketWarning from '../components/websocketWarning';
import { checkAuthenticated, refreshAccessToken, signOut } from '../helpers/auth';
import { config } from '../helpers/constants';

const DiscussionPage = () => {
    const params = useParams();
    const navigate = useNavigate();
    const location = useLocation();
    const currentLocation = location.pathname;

    const [discussionSocket, setDiscussionSocket] = useState(null);
    const [websocketConnected, setwebsocketConnected] = useState(false);
    const [moduleName, setModuleName] = useState('Loading...');
    const [questions, setQuestions] = useState(null);
    const [isLost, setIsLost] = useState(false);
    const [numLost, setNumLost] = useState(0);

    const connectWebSocket = (roomId, accessToken) => {
        const websocketURL = `${config.webSocketProtocol}://${config.serverDomain}/ws/discussion/${roomId}/?token=${accessToken}`

        const discussionSocket = new WebSocket(websocketURL);
        setwebsocketConnected(true);

        discussionSocket.onmessage = (e) => {
            const updatedRoomInfo = JSON.parse(e.data);
            setQuestions(updatedRoomInfo.questions);
            setIsLost(updatedRoomInfo.is_lost);
            setNumLost(updatedRoomInfo.num_lost);
        }

        discussionSocket.onclose = (e) => {
            setwebsocketConnected(false)
        }

        setDiscussionSocket(discussionSocket);
    }

    const handleQuestionInputEnter = (questionInput) => {
        const data = {
            'message': questionInput,
            'message_type': 'question'
        };
        discussionSocket.send(JSON.stringify(data));
    }

    const handleAnswerInputEnter = (answerInput, question_id) => {
        const data = {
            'message': answerInput,
            'message_type': 'answer',
            'question_id': question_id
        };
        discussionSocket.send(JSON.stringify(data));
    }

    const handleQuestionUpvoteButtonClick = (question_id, is_upvote) => {
        const messageType = is_upvote ? 'upvote' : 'downvote'
        const data = {
            'message_type': messageType,
            'question_id': question_id
        }
        discussionSocket.send(JSON.stringify(data));
    }

    const handleIsLostButtonClick = (isLost) => {
        const messageType = isLost ? 'is_lost' : 'is_not_lost'
        const data = {
            'message_type': messageType,
        }
        discussionSocket.send(JSON.stringify(data));
    }

    useEffect(() => {
        const isAuthenticated = checkAuthenticated();
        if (!isAuthenticated) {
            navigate('/signIn', {
                state: {
                    from: currentLocation
                }
            })
        }

        const source = axios.CancelToken.source();
        const roomId = params.roomId;
        const accessToken = localStorage.getItem('access token');

        const getRoomInfo = async (roomId, accessToken) => {
            const httpBaseURL = `${config.httpProtocol}://${config.serverDomain}/discussion/rooms/`;
            const httpURL = httpBaseURL + roomId + '/';

            try {
                const data = await axios.get(httpURL, {
                    headers: { 'Authorization': `Bearer ${accessToken}` },
                    cancelToken: source.token,
                });
                setModuleName(data.data.module);
                setQuestions(data.data.questions);
                setIsLost(data.data.is_lost);
                setNumLost(data.data.num_lost);
            } catch (err) {
                if (err.response.data.code === 'token_not_valid') {
                    const newAccessToken = await refreshAccessToken();
                    if (newAccessToken) {
                        const data = await axios.get(httpURL, {
                            headers: { 'Authorization': `Bearer ${accessToken}` },
                            cancelToken: source.token,
                        });
                        setModuleName(data.data.module);
                        setQuestions(data.data.questions);
                        setIsLost(data.data.is_lost);
                        setNumLost(data.data.num_lost);
                    } else {
                        signOut();
                        navigate('/signIn');
                    }
                } else {
                    navigate('/404');
                }
            }
        }

        getRoomInfo(roomId, accessToken);
        connectWebSocket(roomId, accessToken);

        return () => {
            source.cancel();
        }
    }, [currentLocation])

    return (
        <Box >
            <NavBar />
            <Container>
                <ModuleHeader
                    moduleName={moduleName}
                    isLost={isLost}
                    numLost={numLost}
                    handleIsLostButtonClick={handleIsLostButtonClick}
                />
                {websocketConnected ? null : <WebsocketWarning />}
                <QuestionInput handleQuestionInputEnter={handleQuestionInputEnter} />
                <Questions
                    questions={questions}
                    handleAnswerInputEnter={handleAnswerInputEnter}
                    handleQuestionUpvoteButtonClick={handleQuestionUpvoteButtonClick}
                />
            </Container>
        </Box>
    )
}

export default DiscussionPage;
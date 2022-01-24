import { Routes, Route } from 'react-router-dom';
import HomePage from './views/homePage';
import SignInPage from './views/signInPage';
import DiscussionPage from './views/discussionPage';
import NoPage from './views/noPage';

function App() {
	return (
		<Routes >
			<Route path='/' element={<HomePage />} />
			<Route path='/signin' element={<SignInPage />} />
			<Route path='/:roomId' element={<DiscussionPage />} />
			<Route path='/404' element={<NoPage />} />
			<Route path='*' element={<NoPage />} />
		</Routes >
	);
}

export default App;

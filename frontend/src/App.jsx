import { useState } from 'react'

import './App.css'
import { BrowserRouter as Router, Route, Routes  } from'react-router-dom'

import Login from './pages/Login'
import Register from './pages/Register'
import Chatbot from './components/Chatbot'


function App() {
  return (
    <>
<Router>
      <Routes>
        <Route path='/login' element={<Login/>} />
        <Route path='/register' element={<Register/>} />
        <Route path='/' element={<Chatbot/>} />
        {/* <Route exact path="/history" component={ChatHistory} /> */}
      </Routes >
    </Router>
    </>
  )
}

export default App

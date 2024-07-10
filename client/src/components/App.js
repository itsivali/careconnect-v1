import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import SignUp from './SignUp';
import LogIn from './LogIn';
import Appointment from './Appointment'; 
import Navbar from './Navbar'; 

function App() {
  return (
    <Router>
      <div>
        <Navbar />
        <div className="container mt-4">
          <Switch>
            <Route exact path="/" component={() => <h1>Welcome to the Project Client</h1>} />
            <Route path="/signup" component={SignUp} />
            <Route path="/login" component={LogIn} />
            <Route path="/appointment" component={Appointment} />
          </Switch>
        </div>
      </div>
    </Router>
  );
}

export default App;

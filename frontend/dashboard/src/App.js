import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
import SideNav from "./components/SideNav";
import Main from './components/Main';
import Tasks from './components/Tasks'
import RightSideNav from './components/RightSideNav'
import "./css/app.css";

console.log("okok")

function App() {
  return (
    <div className="App">
      <Router>
        <SideNav />
        <div className="d1"/>
        <Switch>
          <Route path="/" exact component={Main}/> 
          <Route path="/tasks" exact component={Tasks} />
        </Switch>
        <div className="d2"/>
        <RightSideNav />
      </Router>
    </div>
  );
}

export default App;

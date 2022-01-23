import React, { Component } from 'react';
import "../css/app.css";
import {withRouter, Link} from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUserNurse } from '@fortawesome/free-solid-svg-icons'

class SideNav extends Component {


    gotoPaitents = () => {
        this.props.history.push('/');
    }

    gotoTasks = () => {
        this.props.history.push('/tasks');
    }

    gotoMap = () => {
        this.props.history.push('/map');
    }

  render() {
    return (
    <div className="main">
        <div className="navprofile">
            <FontAwesomeIcon className="navprofile-description-i" icon={faUserNurse} />
            <div>
                <div className="navprofile-description-b">Name</div>
                <div className="navprofile-description">Occupation</div>
            </div>
        </div>
        <div className="menu">Menu</div>
        <div className="sidenavlist">
                <ul>
                    <li>
                        <button onClick={this.gotoPaitents}>Patients</button>
                    </li>
                    <li>
                        <button onClick={this.gotoTasks}>Tasks</button>
                    </li>
                    <li>
                        <button onClick={this.gotoMap}>Map</button>
                    </li>
                </ul>
            </div>
    </div>);
  }
}


export default withRouter(SideNav);
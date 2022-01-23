import React, { Component } from 'react';
import "../css/app.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUser } from '@fortawesome/free-solid-svg-icons'

export default class PatientsCard extends Component {
  constructor(props) {
    super(props);

  }

  render() {
    console.log(this.props)
    return (
    <div className="patients-card">
      <div className="p-info">
        <div className="p-pp">
          <FontAwesomeIcon className="p-pic" icon={faUser} />
        </div>
        <div className="p-name">{this.props.name}</div>
      </div>
      <div className="p-main">

      </div>
    </div>
    );
  }
}

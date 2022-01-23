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
        {/* <div>
          New Message >>
        </div> */}
        <div className="pcard-text">
        New Message >> {this.props.text.length > 0 ? this.props.text : "---"}
        </div>
        <div className="pcard-m">
          <div>
            <div>Possible Problems</div>
            <ul>
              {this.props.problems.map(p=>{
                <li>p</li>
              })}
            </ul>
          </div>
          <div className="actions">
            <div>Suggested Actions</div>
            <ul>
              {this.props.actions.map(a=>{
                <li>a</li>
              })}
            </ul>
          </div>
        </div>
      </div>
    </div>
    );
  }
}

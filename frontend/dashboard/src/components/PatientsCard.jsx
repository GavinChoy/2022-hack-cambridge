import React, { Component } from 'react';
import "../css/app.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUser } from '@fortawesome/free-solid-svg-icons'

export default class PatientsCard extends Component {
  constructor(props) {
    super(props);

  }

  render() {
    console.log(this.props.actions)
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
        <div className="pcard-text" style={{fontSize: "20px"}}>
        New Message: {this.props.text.length > 0 ? this.props.text : "---"}
        </div>
        <div className="pcard-m">
          <div style={{width: "50%"}}>
            <div style={{fontSize: "20px"}}>Possible Problems</div>
            <ul>
              {this.props.problems.map(p=>{
                return <li style={{marginTop: "5px"}}>- {p}</li>
              })}
            </ul>
          </div>
          <div className="actions">
            <div style={{fontSize: "20px"}}>Suggested Actions</div>
            <ul>
              {this.props.actions.map(a=>{
                  return <li style={{marginTop: "5px"}}>- {a}</li>
              })}
            </ul>
          </div>
        </div>
      </div>
    </div>
    );
  }
}

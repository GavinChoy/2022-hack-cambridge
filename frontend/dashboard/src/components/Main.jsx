import React, { Component } from 'react';
import PatientsCard from './PatientsCard';
import "../css/app.css";

export default class Main extends Component {
  state = {
    patients: {
      "patient2": [
          {
              "patient_number": "2",
              "problem": [
                  [
                      "fainting",
                      1
                  ],
                  [
                      "shock",
                      1
                  ]
              ],
              "suggested_action": [
                  [
                      "fainting",
                      "bring glucose, check if adrenalin is needed"
                  ],
                  [
                      "shock",
                      "elevate legs, prevent chocking"
                  ]
              ],
              "severity": 2.0,
              "full_text": "cold skin.",
              "time": "2022-01-23T09:43:52.312Z",
              "translated": ""
          }
      ]
  }
  }

  componentDidMount() {
    // this.poll()
  }

  poll = () => {
    const data = {
      "request": "client"
    }
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    headers.append('Accept', 'application/json');
    fetch('https://europe-west2-dementiaassist.cloudfunctions.net/transcription_sentiment', {
      headers: headers,
      mode: "cors",
      method: "POST",
      body: JSON.stringify(data),
    }).then((res)=>{
      // if (res.status !== 202) console.log(res) 
      console.log(res)
      return res.json()
      // this.poll()
    }).then(data=>{
      this.setState({patients: data})
      setTimeout(this.poll, 1000)
    }).catch((err)=>{
      // console.log(err)
      setTimeout(this.poll, 1000)
    }
      )
  }

  render() {
    if (this.state.patients) console.log(this.state.patients)
    return (
    <div className="patients-container">
      <div className="p-t">Patients</div>
      {this.state.patients && Object.keys(this.state.patients).map((key, index) => {
        <PatientsCard 
          name={this.state.patients[key]}
          problems={this.state.patients['patient2'][0]['problem']}
          actions={this.state.patients['patient2'][0]['suggested_action']}
          text={this.state.patients['patient2'][0]['full_text']}
          severity={this.state.patients['patient2'][0]['severity']}
        />
      })}
      <PatientsCard />
    </div>
    );
  }
}

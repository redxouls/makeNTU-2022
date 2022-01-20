import React, { Component } from 'react';
import {ReactFlvPlayer} from 'react-flv-player'

class Index extends Component {

  render() {
    return (
      <div>
        <ReactFlvPlayer
          url = "./test.flv"
          heigh = "800px"
          width = "800px"
          isMuted={true}
        />
      </div>
    );
  }
}
export default Index;
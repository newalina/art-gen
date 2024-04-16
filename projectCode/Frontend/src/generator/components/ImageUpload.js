import React, { Component } from 'react';
import './ImageUpload.css';

class ImageUpload extends Component {
  // state = {
  //   selectedImage: null,
  //   imageURL: ""
  // };

  handleImageChange = (event) => {
    // this.setState({
    //   selectedImage: event.target.files[0],
    //   imageURL: URL.createObjectURL(event.target.files[0])
    // });
    if (event.target.files[0]) {
      this.props.onFileChange(event.target.files[0])
    }
  };

  render() {
    const imageURL =  this.props.files? URL.createObjectURL(this.props.files) : "";

    return (
      <div>        
        {/* {this.state.imageURL && <img src={this.state.imageURL} alt="Uploaded" style={{maxWidth: '500px', maxHeight: '500px'}} />}<br />
        <input type="file" onChange={this.handleImageChange} accept="image/*" /> */}
        {imageURL && <img src={imageURL} alt="Uploaded" style={{maxWidth: '500px', maxHeight: '500px'}} />}<br />
        <input type="file" onChange={this.handleImageChange} accept="image/*" />
      </div>
    );
  }
}

export default ImageUpload;
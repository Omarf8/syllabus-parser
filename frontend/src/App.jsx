import { useState, useRef } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [data, setData] = useState(null)
  const submission = useRef(null)

  const processFile = async () => {
    const file = submission.current.files[0]

    const formData = new FormData()
    formData.append("file", file)

    const response = await fetch("http://127.0.0.1:8000/uploadfile/", {
      method: "POST",
      body: formData
    })

    const data = await response.json()

    setData(data)
  }

  return (
    <div className="syllabus-file">
      <div className="syllabus-upload">
        <div className="column-format">
          <p>Upload A School Syllabus To Extract Important Dates</p>
          <input ref={submission} type="file" id="upload"/>
          <button onClick={processFile}>Confirm</button>
        </div>
      </div>
      <div className="parsed-results">
        <div className="results-box">
          {data ?
          data && 
            data.map((s, index) => (
              <p key={index}>Title: {s.title}, Type: {s.type}, Date: {s.date}, Course: {s.course}</p>
          )) 
          :
          <p>Parsed Results Will Be Shown Here</p>}
        </div>
      </div>
    </div>
  )
}

export default App

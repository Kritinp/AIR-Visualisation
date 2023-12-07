import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { BsFillArchiveFill,BsFillAspectRatioFill,BsFillArrowRightSquareFill, BsFillGrid3X3GapFill, BsPeopleFill, BsFillBellFill } from 'react-icons/bs';

function generateFileNames(n) {
  const fileNames = [];
  for (let i = 0; i <= n; i++) {
    for (let j = 1; j <= 5; j++) {
      fileNames.push(`src/buffers/${i}_${j}_In.txt`);
      fileNames.push(`src/buffers/${i}_${j}_Out.txt`);
    }
  }
  return fileNames;
}

function Home() {
  const [fileData, setFileData] = useState({});
  const [count, setCount] = useState('');
  const [dataflowsCount, setDataflowsCount] = useState(0);
  const [completedWindows, setCompletedWindows] = useState('');
  const [throughput, setThroughput] = useState('');

  const fetchData = async () => {
    try {
      const response1 = await fetch('src/general/count.txt');
      const text1 = await response1.text();
      const newCount = text1.trim().split('\n').slice(-1);
      console.log(newCount);

      const response = await fetch('src/general/df.txt');
      const text = await response.text();
      const n = parseInt(text.trim());

      const windowsResponse = await fetch('src/general/windows.txt');
      const windowsText = await windowsResponse.text();
      const numWindow = windowsText.trim().split('\n').slice(-1);

      const throughputResponse = await fetch('src/general/throughput.txt');
      const throughputText = await throughputResponse.text();
      const throughputValue = throughputText.trim().split('\n').slice(-1);

      const fileNames = generateFileNames(n-1);

      const fetchDataPromises = fileNames.map(async (filePath) => {
        try {
          const response = await fetch(filePath);
          const fileContent = await response.text();
          const allValues = fileContent.trim().split('\n').map(Number);
          const lastThreeValues = allValues.slice(-3);

          const averageValue = lastThreeValues.reduce((acc, val) => acc + val, 0) / lastThreeValues.length;
          const fileNumber = filePath.match(/^src\/buffers\/(\d+)_/)[1];

          return {
            fileName: filePath.slice(12, 19),
            averageValue,
            fileNumber,
          };
        } catch (error) {
          console.error('Error reading file:', error);
          return {
            fileName: filePath,
            averageValue: 0,
            fileNumber: 'unknown',
          };
        }
      });

      const values = await Promise.all(fetchDataPromises);
      console.log(values);
      const groupedData = {};

      values.forEach((file) => {
        const { fileNumber, ...rest } = file;
        if (!groupedData[fileNumber]) {
          groupedData[fileNumber] = [];
        }
        groupedData[fileNumber].push(rest);
      });

      setFileData(groupedData);
      setCount(newCount);
      setDataflowsCount(n);
      setCompletedWindows(numWindow);
      setThroughput(throughputValue);
      
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    fetchData();

    const intervalId = setInterval(() => {
      fetchData();
    }, 5000);

    return () => clearInterval(intervalId);
  }, []);

  const renderBarCharts = () => {
    return Object.entries(fileData).map(([fileNumber, data], index) => {
      const inBars = data.filter(file => file.fileName.includes('_In'));
      const outBars = data.filter(file => file.fileName.includes('_Out'));
  
      const combinedData = inBars.map((inFile, idx) => ({
        fileName: inFile.fileName.slice(0,3),
        In: inFile.averageValue,
        Out: outBars[idx] ? outBars[idx].averageValue : 0,
      }));
  
      return (
        <div key={index} className='chart-container'>
          <h3>Buffers Corresponding to Dataflow: {fileNumber}</h3>
          <div className='charts'>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                width={500}
                height={300}
                data={combinedData}
                margin={{
                  top: 5,
                  right: 30,
                  left: 20,
                  bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="fileName" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="In" name="In" fill="#8884d8" />
                <Bar dataKey="Out" name="Out" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      );
    });
  };


  return (
    <main className='main-container'>
      <div className='main-title'>
        <h3>AIR DASHBOARD</h3>
      </div>

      <div className='main-cards'>
        <div className='card'>
              <div className='card-inner'>
                  <h3>Number of Dataflows</h3>
                  <BsFillArrowRightSquareFill className='card_icon'/>
              </div>
              <h1>{dataflowsCount}</h1>
          </div>
          <div className='card'>
              <div className='card-inner'>
                  <h3>Matches Count</h3>
                  <BsFillGrid3X3GapFill className='card_icon'/>
              </div>
              <h1>{count}</h1>
          </div>
          <div className='card'>
              <div className='card-inner'>
                  <h3>Completed Windows</h3>
                  <BsFillAspectRatioFill className='card_icon'/>
              </div>
              <h1>{completedWindows}</h1>
          </div>
          <div className='card'>
              <div className='card-inner'>
                  <h3>Throughput</h3>
                  <BsFillBellFill className='card_icon'/>
              </div>
              <h1>{throughput}</h1>
          </div>
      </div>

      {renderBarCharts()}
    </main>
  );
}

export default Home;

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar, Pie, Radar } from 'react-chartjs-2';

const AnalyticsDashboard = () => {
    const [analyticsData, setAnalyticsData] = useState(null);

    const fetchAnalytics = async (text) => {
        try {
            const response = await axios.post("http://localhost:8000/api/in-depth-analytics/", { text });
            setAnalyticsData(response.data.analytics_data);
        } catch (error) {
            console.error("Error fetching analytics:", error);
        }
    };

    useEffect(() => {
        const sampleText = "2023 NVIDIA Corporation Annual Review";  // replace with actual text or user input
        fetchAnalytics(sampleText);
    }, []);

    // Example chart configurations (based on assumed structure from Claude's response)
    const financialPerformanceData = {
        labels: ['Revenue', 'Profit', 'Growth Rate'],
        datasets: [
            {
                label: 'Financial Performance',
                data: analyticsData?.financial_performance ? 
                      [analyticsData.financial_performance.revenue, analyticsData.financial_performance.profit, analyticsData.financial_performance.growth_rate] : [],
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
            },
        ],
    };

    const swotData = {
        labels: ['Strengths', 'Weaknesses', 'Opportunities', 'Threats'],
        datasets: [
            {
                label: 'SWOT Analysis',
                data: analyticsData?.swot_analysis ? 
                      [analyticsData.swot_analysis.strengths.length, analyticsData.swot_analysis.weaknesses.length, analyticsData.swot_analysis.opportunities.length, analyticsData.swot_analysis.threats.length] : [],
                backgroundColor: ['rgba(75, 192, 192, 0.6)', 'rgba(255, 99, 132, 0.6)', 'rgba(54, 162, 235, 0.6)', 'rgba(255, 206, 86, 0.6)'],
            },
        ],
    };

    return (
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
            <h1>In-Depth Analytics</h1>

            {analyticsData ? (
                <div>
                    <h2>Financial Performance</h2>
                    <Bar data={financialPerformanceData} options={{ maintainAspectRatio: false }} />

                    <h2>SWOT Analysis</h2>
                    <Radar data={swotData} options={{ maintainAspectRatio: false }} />

                    {/* Add other charts as necessary */}
                </div>
            ) : (
                <p>Loading analytics...</p>
            )}
        </div>
    );
};

export default AnalyticsDashboard;

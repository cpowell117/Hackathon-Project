import './AnalyticsDashboard.css';
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar, Radar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    RadialLinearScale,
    BarElement,
    PointElement,
    LineElement,
    ArcElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    RadialLinearScale,
    BarElement,
    PointElement,
    LineElement,
    ArcElement,
    Title,
    Tooltip,
    Legend
);

const AnalyticsDashboard = ({ analysisText }) => {
    const [analyticsData, setAnalyticsData] = useState(null);
    const [loading, setLoading] = useState(true);  // To handle loading state
    const [error, setError] = useState(false);

    const fetchAnalytics = async (text) => {
        try {
            setLoading(true); 
            const response = await axios.post("http://localhost:8000/api/in-depth-analytics/", { text });
            setAnalyticsData(response.data);
            setError(false);
        } catch (error) {
            console.error("Error fetching analytics:", error);
            setError(true); 
        } finally {
            setLoading(false); 
        }
    };

    useEffect(() => {
        if (analysisText) {  // FFor fetching analytics only if analysisText is available
            fetchAnalytics(analysisText);
        }
    }, [analysisText]);

    const financialPerformanceData = {
        labels: [
            'Timely Payments (Contributory)', 
            'Timely Payments (Reimbursable)', 
            'Receivables Turnover (Contributory)', 
            'Receivables Turnover (Reimbursable)', 
            'Uncollectible Rate (Contributory)', 
            'Uncollectible Rate (Reimbursable)'
        ],
        datasets: [
            {
                label: 'Financial Performance',
                data: [
                    analyticsData?.financial_performance?.timely_payments?.contributory ?? 0, 
                    analyticsData?.financial_performance?.timely_payments?.reimbursable ?? 0, 
                    analyticsData?.financial_performance?.receivables_turnover?.contributory ?? 0, 
                    analyticsData?.financial_performance?.receivables_turnover?.reimbursable ?? 0,
                    analyticsData?.financial_performance?.uncollectible_rate?.contributory ?? 0,
                    analyticsData?.financial_performance?.uncollectible_rate?.reimbursable ?? 0
                ],
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
            },
        ],
    };

    const swotData = {
        labels: ['Strengths', 'Weaknesses', 'Opportunities', 'Threats'],
        datasets: [
            {
                label: 'SWOT Analysis',
                data: [
                    analyticsData?.swot_analysis?.strengths?.length ?? 0, 
                    analyticsData?.swot_analysis?.weaknesses?.length ?? 0, 
                    analyticsData?.swot_analysis?.opportunities?.length ?? 0, 
                    analyticsData?.swot_analysis?.threats?.length ?? 0
                ],
                backgroundColor: ['rgba(75, 192, 192, 0.6)', 'rgba(255, 99, 132, 0.6)', 'rgba(54, 162, 235, 0.6)', 'rgba(255, 206, 86, 0.6)'],
            },
        ],
    };

    console.log("Financial Performance Data:", financialPerformanceData);
    console.log("SWOT Data:", swotData);

    return (
        <div className="analytics-container">
            <h1>In-Depth Analytics</h1>

            {loading ? (
                <p className="loading-text">Loading analytics...</p>
            ) : error ? (
                <p className="error-text">Error fetching analytics data. Please try again later.</p>
            ) : analyticsData ? (
                <div>
                    <div className="chart-container">
                        <h2 className="analytics-section-title">Financial Performance</h2>
                        <Bar data={financialPerformanceData} options={{ maintainAspectRatio: false }} />
                    </div>

                    <div className="chart-container">
                        <h2 className="analytics-section-title">SWOT Analysis</h2>
                        <Radar data={swotData} options={{ maintainAspectRatio: false }} />
                    </div>
                </div>
            ) : (
                <p className="error-text">No analytics available</p>
            )}
        </div>
    );
};

export default AnalyticsDashboard;

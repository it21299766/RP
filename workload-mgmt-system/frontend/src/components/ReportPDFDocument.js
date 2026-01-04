import React from 'react';
import { Document, Page, Text, View, StyleSheet, Image } from '@react-pdf/renderer';

// Create styles
const styles = StyleSheet.create({
  page: {
    flexDirection: 'column',
    backgroundColor: '#FFFFFF',
    padding: 30,
    fontSize: 10,
    fontFamily: 'Helvetica',
  },
  header: {
    marginBottom: 20,
    borderBottom: '2 solid #000000',
    paddingBottom: 10,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 10,
    textAlign: 'center',
  },
  metadata: {
    marginBottom: 5,
    fontSize: 9,
    color: '#666666',
  },
  section: {
    marginTop: 15,
    marginBottom: 10,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  summaryBox: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 5,
    padding: 5,
    backgroundColor: '#F5F5F5',
  },
  summaryLabel: {
    fontWeight: 'bold',
    width: '50%',
  },
  summaryValue: {
    width: '50%',
  },
  table: {
    display: 'table',
    width: 'auto',
    borderStyle: 'solid',
    borderWidth: 1,
    borderRightWidth: 0,
    borderBottomWidth: 0,
    marginTop: 10,
  },
  tableRow: {
    margin: 'auto',
    flexDirection: 'row',
  },
  tableColHeader: {
    width: '12.5%',
    borderStyle: 'solid',
    borderWidth: 1,
    borderLeftWidth: 0,
    borderTopWidth: 0,
    backgroundColor: '#F0F0F0',
    padding: 5,
  },
  tableColHeaderWide: {
    width: '16.67%',
    borderStyle: 'solid',
    borderWidth: 1,
    borderLeftWidth: 0,
    borderTopWidth: 0,
    backgroundColor: '#F0F0F0',
    padding: 5,
  },
  tableCol: {
    width: '12.5%',
    borderStyle: 'solid',
    borderWidth: 1,
    borderLeftWidth: 0,
    borderTopWidth: 0,
    padding: 5,
  },
  tableColWide: {
    width: '16.67%',
    borderStyle: 'solid',
    borderWidth: 1,
    borderLeftWidth: 0,
    borderTopWidth: 0,
    padding: 5,
  },
  tableCellHeader: {
    fontSize: 8,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  tableCell: {
    fontSize: 8,
    textAlign: 'left',
  },
  chartContainer: {
    marginTop: 10,
    marginBottom: 15,
    alignItems: 'center',
    pageBreakInside: 'avoid',
  },
  chartImage: {
    maxWidth: 500,
    maxHeight: 300,
    objectFit: 'contain',
  },
  footer: {
    position: 'absolute',
    bottom: 30,
    left: 30,
    right: 30,
    textAlign: 'center',
    fontSize: 8,
    color: '#666666',
    borderTop: '1 solid #CCCCCC',
    paddingTop: 10,
  },
});

const ReportPDFDocument = ({ reportData, chartImages }) => {
  const { reportType, filters, summary, tableData } = reportData;

  const getReportTitle = () => {
    const titles = {
      'staff-workload-summary': 'Staff Workload Summary',
      'program-teaching-load': 'Program Teaching Load Report',
      'task-assignment': 'Task Assignment Report',
      'underload-overload': 'Underload/Overload Report',
      'ga-optimization': 'GA Optimization Output Report',
      'change-requests': 'Change Requests Report',
      'module-teaching': 'Module-Level Teaching Report',
      'staff-activity': 'Staff Activity Report'
    };
    return titles[reportType] || 'Report';
  };

  const isTaskAssignment = reportType === 'task-assignment';

  return (
    <Document>
      <Page size="A4" style={styles.page}>
        <View style={styles.header}>
          <Text style={styles.title}>{getReportTitle()}</Text>
          <Text style={styles.metadata}>Academic Period: {filters.academicPeriod || 'N/A'}</Text>
          <Text style={styles.metadata}>Semester: {filters.semester}</Text>
          <Text style={styles.metadata}>Generated: {new Date().toLocaleString()}</Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Summary</Text>
          <View style={styles.summaryBox}>
            <Text style={styles.summaryLabel}>Hours Assigned:</Text>
            <Text style={styles.summaryValue}>{summary.hoursAssigned}h</Text>
          </View>
          <View style={styles.summaryBox}>
            <Text style={styles.summaryLabel}>Teaching:</Text>
            <Text style={styles.summaryValue}>{summary.teachingPercent}%</Text>
          </View>
          <View style={styles.summaryBox}>
            <Text style={styles.summaryLabel}>Admin:</Text>
            <Text style={styles.summaryValue}>{summary.adminPercent}%</Text>
          </View>
          <View style={styles.summaryBox}>
            <Text style={styles.summaryLabel}>Research:</Text>
            <Text style={styles.summaryValue}>{summary.researchPercent}%</Text>
          </View>
          <View style={styles.summaryBox}>
            <Text style={styles.summaryLabel}>Overload:</Text>
            <Text style={styles.summaryValue}>{summary.overload ? 'Yes' : 'No'}</Text>
          </View>
        </View>

        {tableData.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Report Data</Text>
            <View style={styles.table}>
              {/* Table Header */}
              <View style={styles.tableRow}>
                {isTaskAssignment ? (
                  <>
                    <View style={styles.tableColHeaderWide}>
                      <Text style={styles.tableCellHeader}>Task Name</Text>
                    </View>
                    <View style={styles.tableColHeaderWide}>
                      <Text style={styles.tableCellHeader}>Staff Name</Text>
                    </View>
                    <View style={styles.tableColHeaderWide}>
                      <Text style={styles.tableCellHeader}>Domain</Text>
                    </View>
                    <View style={styles.tableColHeaderWide}>
                      <Text style={styles.tableCellHeader}>Hrs/Week</Text>
                    </View>
                    <View style={styles.tableColHeaderWide}>
                      <Text style={styles.tableCellHeader}>Total Hrs</Text>
                    </View>
                    <View style={styles.tableColHeaderWide}>
                      <Text style={styles.tableCellHeader}>Method</Text>
                    </View>
                  </>
                ) : (
                  <>
                    <View style={styles.tableColHeader}>
                      <Text style={styles.tableCellHeader}>Staff</Text>
                    </View>
                    <View style={styles.tableColHeader}>
                      <Text style={styles.tableCellHeader}>Domain</Text>
                    </View>
                    <View style={styles.tableColHeader}>
                      <Text style={styles.tableCellHeader}>Tasks</Text>
                    </View>
                    <View style={styles.tableColHeader}>
                      <Text style={styles.tableCellHeader}>Total</Text>
                    </View>
                    <View style={styles.tableColHeader}>
                      <Text style={styles.tableCellHeader}>Teaching</Text>
                    </View>
                    <View style={styles.tableColHeader}>
                      <Text style={styles.tableCellHeader}>Admin</Text>
                    </View>
                    <View style={styles.tableColHeader}>
                      <Text style={styles.tableCellHeader}>Research</Text>
                    </View>
                    <View style={styles.tableColHeader}>
                      <Text style={styles.tableCellHeader}>Status</Text>
                    </View>
                  </>
                )}
              </View>

              {/* Table Rows */}
              {tableData.map((row, index) => (
                <View key={index} style={styles.tableRow}>
                  {isTaskAssignment ? (
                    <>
                      <View style={styles.tableColWide}>
                        <Text style={styles.tableCell}>{row.taskName || 'N/A'}</Text>
                      </View>
                      <View style={styles.tableColWide}>
                        <Text style={styles.tableCell}>{row.staffName || 'N/A'}</Text>
                      </View>
                      <View style={styles.tableColWide}>
                        <Text style={styles.tableCell}>{row.domain || 'N/A'}</Text>
                      </View>
                      <View style={styles.tableColWide}>
                        <Text style={styles.tableCell}>{row.hoursPerWeek || 0}</Text>
                      </View>
                      <View style={styles.tableColWide}>
                        <Text style={styles.tableCell}>{row.totalHours || 0}</Text>
                      </View>
                      <View style={styles.tableColWide}>
                        <Text style={styles.tableCell}>{row.assignmentMethod || 'Manual'}</Text>
                      </View>
                    </>
                  ) : (
                    <>
                      <View style={styles.tableCol}>
                        <Text style={styles.tableCell}>{row.staffName || 'N/A'}</Text>
                      </View>
                      <View style={styles.tableCol}>
                        <Text style={styles.tableCell}>{row.domain || 'N/A'}</Text>
                      </View>
                      <View style={styles.tableCol}>
                        <Text style={styles.tableCell}>{row.tasks || 0}</Text>
                      </View>
                      <View style={styles.tableCol}>
                        <Text style={styles.tableCell}>{row.totalHours || 0}</Text>
                      </View>
                      <View style={styles.tableCol}>
                        <Text style={styles.tableCell}>{row.teachingHours || 0}</Text>
                      </View>
                      <View style={styles.tableCol}>
                        <Text style={styles.tableCell}>{row.adminHours || 0}</Text>
                      </View>
                      <View style={styles.tableCol}>
                        <Text style={styles.tableCell}>{row.researchHours || 0}</Text>
                      </View>
                      <View style={styles.tableCol}>
                        <Text style={styles.tableCell}>{row.status || 'Normal'}</Text>
                      </View>
                    </>
                  )}
                </View>
              ))}
            </View>
          </View>
        )}

        {chartImages && chartImages.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Charts</Text>
            {chartImages.map((chartImage, index) => (
              <View key={index} style={styles.chartContainer}>
                <Image src={chartImage} style={styles.chartImage} />
              </View>
            ))}
          </View>
        )}

        <Text style={styles.footer}>
          Generated by SLIIT - {new Date().toLocaleString()}
        </Text>
      </Page>
    </Document>
  );
};

export default ReportPDFDocument;


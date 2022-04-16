graph [
  DateObtained "16/11/10"
  GeoLocation "USA"
  GeoExtent "Country"
  Network "ATT North America"
  Provenance "Primary"
  Access 0
  Source "http://www.att.com/Common/merger/files/pdf/wired-network/Domestic_0C-768_Network.pdf"
  Version "1.0"
  DateType "Historic"
  Type "COM"
  Backbone 1
  Commercial 0
  label "Example"
  ToolsetVersion "0.3.34dev-20120328"
  Customer 1
  IX 0
  SourceGitVersion "e278b1b"
  DateModifier "="
  DateMonth 0
  LastAccess "3/08/10"
  Layer "IP"
  Creator "Topology Zoo Toolset"
  Developed 1
  Transit 1
  NetworkDate "2007-2008"
  DateYear 0
  LastProcessed "2011_09_01"
  Testbed 0
  node [
    id 0
    label "NY54"
    Country "United States"
    Longitude -74.00597
    Internal 1
    Latitude 40.71427
    type "Completion 2007 - 2008"
  ]
  node [
    id 1
    label "CMBR"
    Country "United States"
    Longitude -71.10561
    Internal 1
    Latitude 42.3751
    type "Completion 2007 - 2008"
  ]
  node [
    id 2
    label "CHCG"
    Country "United States"
    Longitude -87.65005
    Internal 1
    Latitude 41.85003
    type "Completed"
  ]
  node [
    id 3
    label "CLEV"
    Country "United States"
    Longitude -81.69541
    Internal 1
    Latitude 41.4995
    type "Completed"
  ]
  node [
    id 4
    label "RLGH"
    Country "United States"
    Longitude -78.63861
    Internal 1
    Latitude 35.7721
    type "Completion 2007 - 2008"
  ]
  node [
    id 5
    label "ATLN"
    Country "United States"
    Longitude -84.38798
    Internal 1
    Latitude 33.749
    type "Completed"
  ]
  edge [
    source 1
    target 2
    LinkLabel "Completion 2007-2008"
  ]
  edge [
    source 2
    target 3
    LinkLabel "Completed"
  ]
    edge [
    source 3
    target 4
    LinkLabel "Completion 2007-2008"
  ]
  edge [
    source 4
    target 5
    LinkLabel "Completion 2007-2008"
  ]
  edge [
    source 0
    target 1
    LinkLabel "Completed"
  ]
]

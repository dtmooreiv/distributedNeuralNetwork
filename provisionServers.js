var AWS = require("aws-sdk");
var needle = require("needle");
var os = require("os");
var fs = require("fs");

AWS.config.loadFromPath("./awsConfig.json");

// Create the instance, from https://docs.aws.amazon.com/AWSJavaScriptSDK/guide/node-examples.html
var ec2 = new AWS.EC2();

var params = {
  ImageId: 'ami-b141a2f5',
  InstanceType: 'g2.2xlarge', 
  MinCount: 4, MaxCount: 4,
  KeyName: 'mac_aws_west'
};

ec2.runInstances(params, function(err, data) {
  if (err) { console.log("Could not create instance", err); return; }

  var instanceIds = [];
  var contents = '[';

  for(i in data.Instances) {
    contents += (JSON.stringify(data.Instances[i], null, 4) + '\n');
    instanceIds.push(data.Instances[i].InstanceId);
    if(i < data.Instances.length - 1) {
      contents += ',';
    }
  }
  contents += ']'

  fs.writeFile("./ec2.json", contents, function (err) {
    if(err) {
        console.log("Error writing file: " + err);
    }

    console.log("File saved!");
  })

  // Add tags to the instance
  params = {Resources: instanceIds, Tags: [
    {Key: 'Name', Value: 'amazonDigitsServer'}
  ]};
  ec2.createTags(params, function(err) {
    console.log("Tagging instance", err ? "failure" : "success");
  });
});

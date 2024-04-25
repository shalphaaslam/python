var context = $evaluation.getContext();
var identity = context.getIdentity();
var contextAttributes = context.getAttributes();
var userAttributes = identity.getAttributes();
var resource = $evaluation.getPermission().getResource();
var permission = $evaluation.getPermission()

if (identity !== undefined && identity !== null) {
    print("Identity object is initialized and accessible.");

} else {
    print("Identity object is not accessible.");
}

if (permission !== undefined && permission !== null) {
    print("Permission object is initialized and accessible.");
} else {
    print("Permission object is not accessible.");
}


var userAttributesMap = userAttributes.toMap();
// Print all user attributes
var attributeNames = userAttributesMap.keySet().toArray();
for (var i = 0; i < attributeNames.length; i++) {
    var attributeName = attributeNames[i];
    var attributeValue = userAttributesMap.get(attributeName);
    print(attributeName + ": " + attributeValue);
}

// Get the user attribute
// var userAttribute = identity.getAttributes().getValue('resourceType');
var userAttributeCheck = userAttributesMap.get('resourceType')
if (userAttributeCheck !== undefined && userAttributeCheck !== null) {
    var userAttribute = userAttributesMap.get('resourceType')[0];
    print('resType:' + userAttribute)

    // Get the resource name
    var resourceName = resource.getName();
    print('resname: ' + resourceName)

    // Check if the user attribute matches the resource name
    if (userAttribute === resourceName) {
        $evaluation.grant();
    } else {
        $evaluation.deny();
    }
} else {
    $evaluation.deny();
}
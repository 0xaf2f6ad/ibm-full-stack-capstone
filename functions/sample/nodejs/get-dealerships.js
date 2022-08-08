const { CloudantV1 } = require("@ibm-cloud/cloudant");
const { IamAuthenticator } = require("ibm-cloud-sdk-core");

async function main(params) {
  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator,
  });
  cloudant.setServiceUrl(params.COUCH_URL);
  try {
    let output = await cloudant.postAllDocs({
      db: "dealerships",
    });
    if (params.state) {
      return output.result.rows
        .filter((row) => row.doc.state === params.state)
        .map((row) => {
          return {
            id: row.doc.id,
            city: row.doc.city,
            state: row.doc.state,
            st: row.doc.st,
            address: row.doc.address,
            zip: row.doc.zip,
            lat: row.doc.lat,
            long: row.doc.long,
          };
        });
    }
    return output.result.rows.map((row) => {
      return {
        id: row.doc.id,
        city: row.doc.city,
        state: row.doc.state,
        st: row.doc.st,
        address: row.doc.address,
        zip: row.doc.zip,
        lat: row.doc.lat,
        long: row.doc.long,
      };
    });
  } catch (error) {
    return { error: error.description };
  }
}

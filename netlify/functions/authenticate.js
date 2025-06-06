exports.handler = async (event) => {
    const { password } = JSON.parse(event.body || "{}");
    const expected = process.env.ACCESS_PASSWORD;

    if (password === expected) {
        return {
            statusCode: 200,
            body: JSON.stringify({ access: true }),
        };
    }

    return {
        statusCode: 401,
        body: JSON.stringify({ access: false }),
    };
};
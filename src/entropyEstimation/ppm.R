# Load required libraries
library(ppm)
library(readr)
library(stringr)
library(purrr)
library(progressr)
library(getopt)
library(data.table)
library(R.utils)


MAX_TRAIN <- 10000

# Define the command line options
spec <- matrix(c(
  'tokens', 'T', 1, 'character',
  'output_dir', 'O', 1, 'character',
  'max_train', 'M', 1, 'integer',
  'vocab', 'V', 1, 'character',
  'decay', 'D', 1, 'numeric'
), byrow = TRUE, ncol = 4)

args <- getopt(spec)

# Assign default values
tokens_file <- args$tokens
output_dir <- args$output_dir
max_train <- ifelse(is.null(args$max_train), MAX_TRAIN, args$max_train)
vocab_file <- args$vocab
decay <- ifelse(is.null(args$decay), 0, args$decay)
decay <- ifelse(decay == 0, FALSE, TRUE)


print(paste('File:', tokens_file))
print(paste('Vocab:', vocab_file))
print(paste('Output directory:', output_dir))
print(paste('Max train occurence:', max_train))
print(paste('Decay:', decay))


# Function to process a single tweet
process_tweet <- function(tweet, model, decay = FALSE, last_end_time = 1) {
    # Preprocess the tweet
    tokens <- strsplit(gsub('(^\\[|\\]$)', '', tweet), ',(?=(?:[^"]*"[^"]*")*[^"]*$)', perl = TRUE)[[1]]
    tokens <- gsub('^"|"$', '', tokens)
    tokens <- tokens[tokens != '\"\"']
    tokens <- tokens[tokens %in% model$alphabet_levels]  # (should not happen, security check)

    # Convert the tokens to the factor levels based on the vocabulary
    tokens_factor <- match(tokens, model$alphabet_levels)

    # Model the sequence
    if (!decay) {
        res <- model_seq(model, tokens_factor)
    } else {
        time_seq <- seq_along(tokens_factor) + last_end_time
        res <- model_seq(model, tokens_factor, time = time_seq)
        last_end_time <- max(time_seq)
    }

    # Return the average entropy
    list(avg_entropy = mean(res$entropy, na.rm = TRUE), entropy = res$entropy, last_end_time = last_end_time, model_order = res$model_order, information_content = res$information_content)
}


generate_result <- function(nbr_trained) {
    # PREDICTION 50 tokens
    if (decay) {
        seq_time <- seq(1, 50) + last_end_time
        pred <- model_seq(model, generate = TRUE, seq = 50, time = seq_time)
    } else {
        pred <- model_seq(model, generate = TRUE, seq = 50)
    }

    # Compute the average statistics
    model_order_matrix <- matrix(NA, nrow = length(model_order), ncol = max(sapply(model_order, length)))
    information_content_matrix <- matrix(NA, nrow = length(information_content), ncol = max(sapply(information_content, length)))
    entropy_matrix <- matrix(NA, nrow = length(entropy), ncol = max(sapply(entropy, length)))

    for (i in seq_along(model_order)) {
        model_order_matrix[i, seq_along(model_order[[i]])] <- model_order[[i]]
        information_content_matrix[i, seq_along(information_content[[i]])] <- information_content[[i]]
        entropy_matrix[i, seq_along(entropy[[i]])] <- entropy[[i]]
    }

    avg_model_order <- colMeans(model_order_matrix, na.rm = TRUE)
    avg_information_content <- colMeans(information_content_matrix, na.rm = TRUE)
    avg_entropy <- colMeans(entropy_matrix, na.rm = TRUE)

    png(file.path(output_dir, paste0("ppm_model_order_", nbr_trained, ifelse(decay, "_decay", ""), ".png")))
    plot(avg_model_order, type = "l", xlab = "Token Position", ylab = "Average Model Order")
    title(main = "PPM Model Order")
    mtext(paste("Train on:", nbr_trained, "occurences, Decay:", decay), side = 1, line = 4, cex = 0.8)
    mtext(paste("Average Model Order:", round(mean(avg_model_order), 2)), side = 3, line = 0.5, cex = 0.8)
    dev.off()

    png(file.path(output_dir, paste0("ppm_information_content_", nbr_trained, ifelse(decay, "_decay", ""), ".png")))
    plot(avg_information_content, type = "l", xlab = "Token Position", ylab = "Average Information Content (bits)")
    title(main = "PPM Information Content")
    mtext(paste("Train on:", nbr_trained, "occurences, Decay:", decay), side = 1, line = 4, cex = 0.8)
    mtext(paste("Average Information Content:", round(mean(avg_information_content), 2)), side = 3, line = 0.5, cex = 0.8)
    dev.off()

    png(file.path(output_dir, paste0("ppm_entropy_", nbr_trained, ifelse(decay, "_decay", ""), ".png")))
    plot(avg_entropy, type = "l", xlab = "Token Position", ylab = "Average Entropy (bits)")
    title(main = "PPM Entropy")
    mtext(paste("Train on:", nbr_trained, "occurences, Decay:", decay), side = 1, line = 4, cex = 0.8)
    mtext(paste("Average Entropy:", round(mean(avg_entropy), 2)), side = 3, line = 0.5, cex = 0.8)
    dev.off()

    png(file.path(output_dir, paste0("ppm_entropy_distribution_", nbr_trained, ifelse(decay, "_decay", ""), ".png")))
    hist(avg_entropy_tweet[1:nbr_trained], breaks = 20, main = "PPM Entropy Distribution", xlab = "Entropy (bits)", freq = FALSE)
    lines(density(avg_entropy_tweet[1:nbr_trained]), col = "black")
    abline(v = mean(avg_entropy_tweet[1:nbr_trained]), col = "red")
    mtext(paste("Train on:", nbr_trained, "occurences, Decay:", decay), side = 1, line = 4, cex = 0.8)
    mtext(paste("Average Entropy:", round(mean(avg_entropy_tweet[1:nbr_trained]), 2)), side = 3, line = 0.5, cex = 0.8)
    dev.off()


    # Save the results
    write.table(avg_model_order, file.path(output_dir, paste0("ppm_model_order_", nbr_trained, ifelse(decay, "_decay", ""), ".txt")), row.names = FALSE, col.names = FALSE)
    write.table(avg_information_content, file.path(output_dir, paste0("ppm_information_content_", nbr_trained, ifelse(decay, "_decay", ""), ".txt")), row.names = FALSE, col.names = FALSE)
    write.table(avg_entropy, file.path(output_dir, paste0("ppm_entropy_", nbr_trained, ifelse(decay, "_decay", ""), ".txt")), row.names = FALSE, col.names = FALSE)
    write.table(avg_entropy_tweet[1:nbr_trained], file.path(output_dir, paste0("ppm_entropy_distribution_", nbr_trained, ifelse(decay, "_decay", ""), ".txt")), row.names = FALSE, col.names = FALSE)

    prediction_msg <- paste("Prediction:", paste(pred$symbol, collapse = " "))

    write.table(prediction_msg, file.path(output_dir, paste0("ppm_prediction_", nbr_trained, ifelse(decay, "_decay", ""), ".txt")), row.names = FALSE, col.names = FALSE)

    print(prediction_msg)
    print(paste0("Average Entropy:", round(mean(avg_entropy_tweet[1:nbr_trained]), 2)))

}

# Main analysis
vocab <- readLines(vocab_file)
vocab_size <- length(vocab)
# vocab_factor <- factor(vocab, levels = vocab)

# Determine the total number of lines
total_lines <- countLines(tokens_file)
if (max_train < total_lines) {
    print(paste("Sampling", max_train, "occurrences"))
    sampled_lines <- rep(FALSE, total_lines)
    sampled_lines[sample(total_lines, max_train)] <- TRUE
} else {
    max_train <- total_lines
    sampled_lines <- rep(TRUE, total_lines)
}


if (!decay) {
    model <- new_ppm_simple(alphabet_size = vocab_size, alphabet_levels = vocab)
} else {
    print("Using decay")
    model <- new_ppm_decay(alphabet_size = vocab_size, alphabet_levels = vocab)
}
rm(vocab)


# Create a text progress bar
pb <- txtProgressBar(min = 0, max = max_train, style = 3)

# Create a vector to store the entropies
avg_entropy_tweet <- numeric(max_train)
model_order <- vector("list", max_train)
information_content <- vector("list", max_train)
entropy <- vector("list", max_train)
last_end_time <- 1

# Initialize line counter
counter <- 1

# open the file connection
con <- file(tokens_file, open = "r")

for (i in seq_len(total_lines)) {
    # Read specific line based on the sample
    line <- readLines(con, n = 1)

    # Process the tweet only if it's in the sampled indexes
    if (sampled_lines[i]) {
        res <- process_tweet(line, model = model, decay = decay, last_end_time = last_end_time)
        last_end_time <- res$last_end_time
        avg_entropy_tweet[counter] <- res$avg_entropy
        entropy[[counter]] <- res$entropy
        model_order[[counter]] <- res$model_order
        information_content[[counter]] <- res$information_content
        # Update the progress bar
        setTxtProgressBar(pb, counter)


        # every 1000 tweets, save the results
        if (counter %% 1000 == 0) {
            generate_result(counter)
            if (decay) {
                last_end_time <- last_end_time + 50 # add 50 to the last end time due to the prediction
            }
        }
        counter <- counter + 1
    }
}

# Close file connection
close(con)
